import os
import json
import tiktoken
import chromadb
import openai
import numpy as np
CHUNK_SIZE = 180
OVERLAP = 30
DATABASE_CONFIG_PATH = '/app/config/database.json'
DOCUMENTS_PATH = '/data/documents/'
COLLECTION_NAME = 'company_faq_docs'
EMBEDDING_DIM = 1536
openai.api_key = os.environ.get('OPENAI_API_KEY', 'sk-placeholder')
enc = tiktoken.get_encoding('cl100k_base')
def tokenize(text):
    return enc.encode(text)
def chunk_faqs(text, chunk_size=CHUNK_SIZE, overlap=OVERLAP):
    tokens = tokenize(text)
    total = len(tokens)
    chunks = []
    i = 0
    while i < total:
        chunk_tokens = tokens[i:i+chunk_size]
        chunk_text = enc.decode(chunk_tokens)
        chunks.append((i, chunk_text))
        i += chunk_size - overlap
    return chunks
with open(DATABASE_CONFIG_PATH) as f:
    db_cfg = json.load(f)
client = chromadb.Client(chromadb.config.Settings(chroma_db_impl="duckdb+parquet", persist_directory=db_cfg['persist_directory']))
collection_names = [c.name for c in client.list_collections()]
if COLLECTION_NAME not in collection_names:
    collection = client.create_collection(COLLECTION_NAME)
else:
    collection = client.get_collection(COLLECTION_NAME)
for fname in os.listdir(DOCUMENTS_PATH):
    if not fname.endswith('.txt'): continue
    with open(os.path.join(DOCUMENTS_PATH, fname),'r') as f:
        content = f.read()
    faqs = [block.strip() for block in content.split('\n\n') if block.strip()]
    for k, block in enumerate(faqs):
        cks = chunk_faqs(block)
        chunk_ids, embeds, metas, docs = [], [], [], []
        for j, (start_tok, c_text) in enumerate(cks):
            tokens = tokenize(c_text)
            doc_id = f'{fname}_b{k}_c{j}'
            meta = {
                'doc_id': fname,
                'category': fname.split('_')[0].replace('faq','').replace('.txt','').strip() or 'general',
                'chunk_index': j,
                'title': c_text.split('\n')[0][:100],
                'citation_url': f'https://kb.company.com/{fname}#{k}',
                'token_count': len(tokens)
            }
            chunk_ids.append(doc_id)
            docs.append(c_text)
            metas.append(meta)
        if docs:
            batch_embeds = []
            for doc in docs:
                vec = openai.Embedding.create(input=doc, model="text-embedding-ada-002")['data'][0]['embedding']
                batch_embeds.append(vec)
            collection.upsert(ids=chunk_ids, embeddings=batch_embeds, metadatas=metas, documents=docs)
print('FAQ processing and embedding complete.')
