from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_openai import ChatOpenAI
from langchain_core.documents import Document
from neo4j import GraphDatabase
import html2text

def connect_to_neo4j(uri, user, password):
    driver = GraphDatabase.driver(uri, auth=(user, password))
    return driver

def insert_nodes_and_relationships(driver, nodes, relationships):
    with driver.session() as session:
        # Chèn nodes
        for node in nodes:
            cypher_query = f"""
                MERGE (n:{node.type} {{id: $id}})
                SET n += $properties
            """
            session.run(
                cypher_query,
                id=node.id,
                properties=node.properties
            )

        # Chèn relationships
        for relationship in relationships:
            cypher_query = f"""
                MATCH (a:{relationship.source.type} {{id: $source_id}}), 
                      (b:{relationship.target.type} {{id: $target_id}})
                MERGE (a)-[r:{relationship.type}]->(b)
                SET r += $properties
            """
            session.run(
                cypher_query,
                source_id=relationship.source.id,
                target_id=relationship.target.id,
                properties=relationship.properties
            )

llm = ChatOpenAI(temperature=0, model_name="gpt-4o")
llm_transformer = LLMGraphTransformer(llm=llm,node_properties=True)

def html_to_markdown(html_content):
    """
    Convert HTML content to Markdown format.

    :param html_content: The HTML content as a string
    :return: Converted Markdown content as a string
    """
    h = html2text.HTML2Text()
    h.ignore_links = False  # Set to True if you want to ignore links
    h.ignore_images = False  # Set to True if you want to ignore images
    markdown_content = h.handle(html_content)
    return markdown_content

with open('input/dai-hoc-kinh-te-quoc-dan-KHA.html', 'r') as file:
    file_content = file.read()
    markdown_content = html_to_markdown(file_content)

text = markdown_content
documents = [Document(page_content=text)]
graph_documents = llm_transformer.convert_to_graph_documents(documents)
print(f"Nodes:{graph_documents[0].nodes}")
print(f"Relationships:{graph_documents[0].relationships}")

# Kết nối đến Neo4j
uri = "bolt://neo4j:7687"
user = "neo4j"
password = "password"
driver = connect_to_neo4j(uri, user, password)

# Lấy nodes và relationships từ graph_documents
nodes = graph_documents[0].nodes
relationships = graph_documents[0].relationships

# Chèn dữ liệu vào Neo4j
insert_nodes_and_relationships(driver, nodes, relationships)

# Đóng kết nối Neo4j
driver.close()

print("Nodes and relationships inserted into Neo4j.")