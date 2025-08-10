import json
import chromadb
with open('/app/config/database.json') as f:
    cfg = json.load(f)
client = chromadb.Client(chromadb.config.Settings(chroma_db_impl="duckdb+parquet", persist_directory=cfg['persist_directory']))
col = client.get_collection('company_faq_docs')
def verify():
    print(f"Collection: {col.name}, {col.count()} chunks present.")
    ex = col.peek(3)
    print(f"Sample docs: {[d[:60] for d in ex['documents']]}")
    print(f"Dimensions: {len(ex['embeddings'][0])}")
    print(f"Sample metadata: {ex['metadatas'][0]}")
if __name__ == '__main__':
    verify()
