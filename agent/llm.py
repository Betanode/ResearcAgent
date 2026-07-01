from langchain_ollama import ChatOllama

def get_llm():

    return ChatOllama(

        model="qwen2.5:7b-instruct",
        temperature=0,
        num_ctx=8192,
        num_predict=1024,
        repeat_penalty=1.1,
        top_p=0.9,
        top_k=40,
        keep_alive="10m",
    )