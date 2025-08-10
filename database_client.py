import chromadb
import json
with open('config/database.json') as f:
    db_cfg = json.load(f)
COLLECTION_NAME = 'company_faq_docs'
DB_PATH = db_cfg['persist_directory']
class ChromaFAQClient:
    def __init__(self):
        self.client = chromadb.Client(chromadb.config.Settings(chroma_db_impl="duckdb+parquet", persist_directory=DB_PATH))
        self.collection = self.client.get_collection(COLLECTION_NAME)
    def vector_search(self, embedding, top_k=5, category=None):
        pass
    def get_chunk_by_id(self, doc_id):
        pass
    def get_chunks_by_category(self, category):
        pass
