from typing import List, Dict, Any, Optional
class FAQRAGPipeline:
    def __init__(self, db_client):
        self.db_client = db_client
    def encode_query(self, question: str) -> List[float]:
        """
        Encode user query into an embedding vector (1536 floats).
        Input: question text
        Output: list of floats
        """
        pass
    def retrieve_top_k(self, query_embedding: List[float], k: int = 6, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Perform top-K ANN vector search and (optional) category filter.
        Input: query embedding, k, category (optional)
        Output: List of chunk dicts (content, metadata)
        """
        pass
    def build_context(self, retrieved_chunks: List[Dict[str, Any]], max_tokens: int = 1200) -> str:
        """
        Assemble context for LLM generation, ensuring window <= max_tokens and adding citation markers.
        Input: list of chunks, max token limit
        Output: formatted context string
        """
        pass
    def build_prompt(self, query: str, context: str) -> str:
        """
        Compose the prompt for the LLM, including system/user sections and citation guidance.
        Input: user query, retrieved context (with citations)
        Output: prompt string
        """
        pass
    def log_metrics(self, timings: Dict[str,float], tokens_used: int, retrieved: int, response_len: int):
        """
        Log latency, tokens, retrieved count, and response length per query.
        """
        pass
    def evaluate_query(self, query: str, gold_answers: List[str], topk_retrieved: List[Dict[str,Any]]):
        """
        Compute recall@k and log evaluation summary for iterative tuning.
        """
        pass
