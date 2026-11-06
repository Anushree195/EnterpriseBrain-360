from knowledge.rag_service import build_rag_prompt
from knowledge.llm_service import generate_answer


query = "How can organizations optimize Azure cloud infrastructure costs?"

try:
    print("\nBuilding RAG prompt...")

    rag_result = build_rag_prompt(
        query=query,
        top_k=3
    )

    if not rag_result["sources"]:
        print("No relevant documents found.")
        raise SystemExit(0)

    print("Retrieved", len(rag_result["sources"]), "document chunks.")

    print("\nGenerating answer using Ollama...")

    answer = generate_answer(rag_result["prompt"])

    print("\n====================================")
    print("ENTERPRISEBRAIN 360 - AI RESPONSE")
    print("====================================")

    print("\nQuestion:")
    print(query)

    print("\nAI Answer:")
    print(answer)

    print("\nSources:")

    for source in rag_result["sources"]:
        print(
            f"- {source['source']} "
            f"(Page {source['page_number']})"
        )

except Exception as error:
    print("\nRAG generation failed!")
    print("Error:", error)