from knowledge.rag_service import build_rag_prompt


query = "How can organizations optimize Azure cloud infrastructure costs?"

try:
    result = build_rag_prompt(
        query=query,
        top_k=3
    )

    print("\nRAG Prompt Construction Successful!")
    print("====================================")

    print("\nUser Question:")
    print(result["query"])

    print("\nRetrieved Sources:")

    for source in result["sources"]:
        print(
            f"- {source['source']} | "
            f"Page: {source['page_number']} | "
            f"Distance: {source['distance']:.4f}"
        )

    print("\nGenerated Prompt:")
    print(result["prompt"])

except Exception as error:
    print("\nRAG prompt construction failed!")
    print("Error:", error)