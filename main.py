from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="llama3.2:1b"
)

response = llm.invoke("Whats 2 + 2 ?")

print(response.content)