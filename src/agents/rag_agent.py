from typing import TypedDict, List
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import Document
from langgraph.graph import StateGraph, END
from src.loaders.vector_store import VectorStoreManager

class AgentState(TypedDict):
    query: str
    context: List[Document]
    response: str

class RAGAgent:
    def __init__(self, api_key: str, model_name: str, vector_store: VectorStoreManager):
        self.llm = ChatGoogleGenerativeAI(
            model=model_name,
            google_api_key=api_key,
            temperature=0.7
        )
        self.vector_store = vector_store
        self.graph = self._build_graph()
    
    def _retrieve_context(self, state: AgentState) -> AgentState:
        query = state["query"]
        docs = self.vector_store.search(query, k=4)
        state["context"] = docs
        return state
    
    def _generate_response(self, state: AgentState) -> AgentState:
        query = state["query"]
        context = state["context"]
        
        if not context:
            state["response"] = "I couldn't find relevant information to answer your question."
            return state
        
        # combine context from retrieved docs
        context_text = "\n\n".join([
            f"Source: {doc.metadata.get('title', 'Unknown')}\n{doc.page_content[:500]}..."
            for doc in context
        ])
        
        prompt = f"""Based on the following context, answer the question.
If the answer is not in the context, say you don't know.

Context:
{context_text}

Question: {query}

Answer:"""
        
        response = self.llm.invoke(prompt)
        state["response"] = response.content
        return state
    
    def _build_graph(self):
        workflow = StateGraph(AgentState)
        
        workflow.add_node("retrieve", self._retrieve_context)
        workflow.add_node("generate", self._generate_response)
        
        workflow.set_entry_point("retrieve")
        workflow.add_edge("retrieve", "generate")
        workflow.add_edge("generate", END)
        
        return workflow.compile()
    
    def run(self, query: str) -> str:
        initial_state = {
            "query": query,
            "context": [],
            "response": ""
        }
        
        result = self.graph.invoke(initial_state)
        return result["response"]
