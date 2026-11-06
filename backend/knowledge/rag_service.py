
from knowledge.vector_store import search_chunks


def build_rag_prompt(
    query: str,
    top_k: int = 3
) -> dict:
    """
    Retrieve relevant document chunks and build
    a concise, context-grounded RAG prompt.
    """

    # 1. Validate the question
    if not query or not query.strip():
        raise ValueError("Question cannot be empty.")

    if top_k <= 0:
        raise ValueError("top_k must be greater than zero.")

    # 2. Retrieve relevant chunks
    retrieved_chunks = search_chunks(
        query=query,
        top_k=top_k
    )

    # 3. Handle empty knowledge base
    if not retrieved_chunks:
        return {
            "query": query,
            "context": "",
            "sources": [],
            "prompt": ""
        }

    context_parts = []
    sources = []

    # 4. Build context and source references
    for index, chunk in enumerate(retrieved_chunks, start=1):

        metadata = chunk["metadata"]

        source = metadata["source"]
        page_number = metadata["page_number"]

        context_parts.append(
            f"""
[Source {index}, Page {page_number}]
Document: {source}

Content:
{chunk["text"]}
"""
        )

        sources.append({
            "source_number": index,
            "source": source,
            "page_number": page_number,
            "distance": chunk["distance"]
        })

    context = "\n".join(context_parts)

    # 5. Construct the improved RAG prompt
    prompt = f"""
You are EnterpriseBrain 360, an enterprise knowledge assistant.

Answer the user's question using ONLY the retrieved
document context provided below.

STRICT ANSWERING RULES:

1. Include only information directly relevant to the question.
2. Do not introduce unrelated facts from the retrieved context.
3. Do not use outside knowledge or invent information.
4. Combine related information into concise bullet points.
5. Avoid repeating the same recommendation or fact.
6. Include only useful details that answer the question.
7. Every factual bullet must have an inline citation.
8. Use the exact citation format:
   [Source 1, Page 4]
9. Source numbers and page numbers must match the context.
10. Never invent citations or page numbers.
11. If multiple sources support a claim, cite each relevant source.
12. If the context does not contain enough information,
    clearly explain what information is missing.
13. If the question is unrelated to the retrieved context,
    say that the available documents do not contain
    relevant information to answer it.
14. Do not repeat the same information in a summary
    and then again in separate bullet points.
15. Do not add a separate generic introduction or conclusion.

OUTPUT FORMAT:

- Provide 2 to 5 concise bullet points when sufficient
  information is available.
- Each bullet should communicate one distinct point.
- Put the citation at the end of each factual bullet.
- Do not include a separate Sources section in the answer.
  Source metadata is returned separately by the application.

RETRIEVED DOCUMENT CONTEXT:

{context}

USER QUESTION:

{query}

Now provide a concise, relevant and accurate answer.
"""

    return {
        "query": query,
        "context": context,
        "sources": sources,
        "prompt": prompt
    }
