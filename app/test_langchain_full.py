from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_neo4j import GraphCypherQAChain, Neo4jGraph
from langchain_openai import ChatOpenAI

graph = Neo4jGraph(url="bolt://neo4j:7687", username="neo4j", password="password", enhanced_schema=True)

print(graph.schema)

# Tập tập vào duy cấu trúc

chain = GraphCypherQAChain.from_llm(
    ChatOpenAI(temperature=0),
    graph=graph,
    verbose=True,
    top_k=5,
    allow_dangerous_requests=True,
)

# result = chain.invoke({"query": "Giáo dục Đặc biệt có mã ngành (code) là gì?"})
# print(f"Final answer: {result['result']}")

result = chain.invoke({"query": "National Economics University có những Admission_method tuyển gì?"})

print(f"Final answer: {result['result']}")