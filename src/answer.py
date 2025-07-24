from ollama import chat

def retrieve(query: str, vectorstore, k: int = 3):
    """
    Retrieves relevant text chunks or image descriptions.
    """
    results = vectorstore.similarity_search(query, k=k)
    context = "\n\n".join([doc.page_content for doc in results])
    return context

def generate_answer(query: str, context: str,preview:str,data) -> str:
    """
    Generates an answer based on the retrieved context (text or image descriptions).
    """
    system_prompt = """
    You are a data visualization assistant.

Your job is to create Vega-Lite JSON specifications that can be rendered Streamlit.

Rules:
- DO NOT write or return Python code.
- DO NOT use `exec()`, `eval()`, or any Python-specific functions.
- Output ONLY valid Vega-Lite JSON inside a markdown code block.
- DO NOT use the data property as the data would be provided by the user.
- Do NOT include real data in the JSON.
- ALWAYS include a "mark" key
- Title the chart and label axes clearly.
- Use the latest Vega-Lite v6 schema: "https://vega.github.io/schema/vega-lite/v6.json"

Assume the user has uploaded a pandas DataFrame called 'df'.
At the end of your response, do NOT include any explanation or notes—ONLY output the chart spec in a code block.
If no context is provided, answer conversationally.
Here is the preview of the data:\n"""+preview+"\n Here is the summary of data look:\n"+data

    if context.strip():
        # Case 1: Context is available (text or image description)
        user_content = f"Context: {context}\n\nQuestion: {query}"
    else:
        # Case 2: No context, just a conversational query
        user_content = query

    response = chat(
        model="qwen2.5-coder:latest",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content}
        ]
    )

    return response["message"]["content"]