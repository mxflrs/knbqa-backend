from typing import Dict, List, Any, Callable, Optional
import uuid
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import chain
from langgraph.graph import END, StateGraph

from app.config import settings
from app.schemas.qa import ChainNode, ChainEdge, ChainVisualization

class QAChain:
    # CHAIN COMBINES RETRIEVAL WITH GEN AND TRACES THE EXEC
    
    def __init__(self, retriever_fn: Callable):
        self.llm = ChatOpenAI(
            model=settings.LLM_MODEL,
            temperature=0,
            api_key=settings.OPENAI_API_KEY,
            streaming=True
        )
        self.retriever_fn = retriever_fn
        self.graph = self._build_graph()
        self.trace_data = {
            "nodes": [],
            "edges": []
        }
        self.node_counter = 0
    
    
    def _get_node_id(self, prefix: str) -> str:
        # GENERATE A UNIQUE NODE ID WITH PREFIX
        self.node_counter += 1
        return f"{prefix}_{self.node_counter}"
    
    def _add_to_trace(self, 
                      content: str, 
                      node_type: str, 
                      source_id: Optional[str] = None,
                      edge_label: Optional[str] = None,
                      metadata: Optional[Dict[str, Any]] = None) -> str:
        # ADD A NODE AND OPT AND EDGE TO THE TRACE
        node_id = self._get_node_id(node_type)
        
        # ADD NODE
        self.trace_data["nodes"].append({
            "id": node_id,
            "type": node_type,
            "content": content,
            "metadata": metadata or {}
        })
        
        # ADD EDGE IF SOURCE ID PROVIDED
        if source_id:
            self.trace_data["edges"].append({
                "source": source_id,
                "target": node_id,
                "label": edge_label
            })
        
        return node_id
    
    def _retrieve_context(self, state: Dict[str, Any]) -> Dict[str, Any]:
        question = state["question"]
        
        # ADD QUESTION TO TRACE
        question_id = self._add_to_trace(
            content=question,
            node_type="question"
        )
        
        # RETRIEVE RELEVANT CHUNKS
        retrieved_chunks = self.retriever_fn(question)
        
        # UPDATE STATE WITH RETRIEVED CONTEXT
        context_texts = []
        for chunk in retrieved_chunks:
            chunk_id = self._add_to_trace(
                content=chunk["content"],
                node_type="context",
                source_id=question_id,
                edge_label="retrieves",
                metadata={"similarity": chunk["similarity"]}
            )
            context_texts.append(chunk["content"])
        
        # JOIN CONTEXT
        context = "\n\n".join(context_texts)
        state["context"] = context
        state["question_node_id"] = question_id
        return state
    
    def _generate_answer(self, state: Dict[str, Any]) -> Dict[str, Any]:
        # GEN ANSWER BASED ON
        question = state["question"]
        context = state["context"]
        question_node_id = state["question_node_id"]
        
        prompt_template = """
        Answer the question based only on the provided context. If the context doesn't contain 
        the information needed to answer the question, reply with "I don't have enough information 
        to answer this question."
        
        Context:
        {context}
        
        Question: {question}
        
        Answer:
        """
        
        prompt = ChatPromptTemplate.from_template(prompt_template)
        
        # ADD REASONING
        reasoning_id = self._add_to_trace(
            content="Analyzing context and formulating answer...",
            node_type="reasoning",
            source_id=question_node_id,
            edge_label="reasons"
        )
        
        # GENERATE ANSWER
        chain = prompt | self.llm | StrOutputParser()
        answer = chain.invoke({"context": context, "question": question})
        
        # ADD NODE TO TRACE
        answer_id = self._add_to_trace(
            content=answer,
            node_type="answer",
            source_id=reasoning_id,
            edge_label="produces"
        )
        
        state["answer"] = answer
        return state
    
    def _build_graph(self) -> StateGraph:
        # BUILD THE STATE GRAPH FOR THE QA CHAIN
        workflow = StateGraph({"question": str, "context": str, "answer": str, "question_node_id": str})
        
        # ADD NODES FOR EACH STEP
        workflow.add_node("retrieve_context", self._retrieve_context)
        workflow.add_node("generate_answer", self._generate_answer)
        
        # CONNECT THE NODES
        workflow.set_entry_point("retrieve_context")
        workflow.add_edge("retrieve_context", "generate_answer")
        workflow.add_edge("generate_answer", END)
        
        return workflow.compile()
    
    def run(self, question: str) -> Dict[str, Any]:
        self.trace_data = {
            "nodes": [],
            "edges": []
        }
        self.node_counter = 0
        
        # RUN GRAPH
        result = self.graph.invoke({"question": question})
        
        # CONVERT TRACE DATA TO PROPER SCHEMA
        nodes = [ChainNode(**node) for node in self.trace_data["nodes"]]
        edges = [ChainEdge(**edge) for edge in self.trace_data["edges"]]
        
        chain_visualization = ChainVisualization(nodes=nodes, edges=edges)
        
        return {
            "question": question,
            "answer": result["answer"],
            "chain_visualization": chain_visualization
        }