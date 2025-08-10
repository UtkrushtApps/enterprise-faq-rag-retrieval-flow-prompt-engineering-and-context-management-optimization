# Task Overview
Your objective is to complete the semantic retrieval and answer generation pipeline for a company Q&A assistant. You'll assemble a high-quality RAG (Retrieval-Augmented Generation) flow: encode incoming questions, retrieve the most relevant knowledge chunks, manage context windows for LLMs, add inline citations, enable simple category filters, and ensure accurate, traceable, and concise responses for end users.

## Guidance
- Implement core retrieval and pipeline logic focusing on optimizing the relevance of answers, efficiency of search, and clarity of responses.
- Construct prompts that show sourced context (with inline citation markers), fit the model's token constraints, and guide the LLM to generate clear, referenced answers.
- Log and monitor search/generation times, token usage, and top-k retrieval diagnostics to support future tuning and evaluation.
- Ensure the system can filter results by question category. Provide easily understandable, well-structured outputs for both user and business needs.

## Database Access Information
- Vector DB: Chroma running as container `chroma_faq_db` (port 8000)
- Embeddings: OpenAI ada-002, 1536 dimensions
- Collection: `company_faq_docs`
- Metadata per chunk: `doc_id`, `title`, `category`, `chunk_index`, `content`, `citation_url`, `token_count`, `embed` (1536 floats)
- Use `database_client.py` to perform vector search or filter by category as needed. All database operations and document population are automated.

## Objectives
- Complete and optimize RAG pipeline in `rag_pipeline.py` for: encoding queries, performing top-k search, context management, prompt engineering, traceable answers, filter support, and evaluation hooks.
- Outcomes should: (a) improve answer precision, (b) minimize irrelevant context, (c) always display at least one citation, and (d) log latency/token metrics per request.

## How To Verify
- Run the provided queries in `sample_queries.txt` and check that search/generation metrics are logged.
- Inspect answer quality for single/multi-chunk queries, detection of category filters, and presence of citation inline markers (e.g., [1], [2]).
- Check CSV logs for recall@k computation, token counts, and search/generation latency.
- Confirm responses do not exceed LLM token windows and that answers include only relevant, in-context information.