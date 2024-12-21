from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_openai import ChatOpenAI
from langchain_core.documents import Document
import html2text


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