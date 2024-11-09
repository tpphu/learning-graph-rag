from py2neo import Graph, Node
import pandas as pd

# Kết nối tới cơ sở dữ liệu Neo4j
graph = Graph("bolt://neo4j:7687", auth=("neo4j", "password"))

# Đọc dữ liệu từ file CSV
csv_file_path = "university_training_programs.csv"
df = pd.read_csv(csv_file_path)

# Chèn dữ liệu vào Neo4j
for index, row in df.iterrows():
    # Tạo Node cho ngành đào tạo
    program_node = Node(
        "UniversityProgram",
        code=row["Mã ngành"],
        name=row["Tên ngành"],
        effectiveness=row["Hiệu lực"] if "Hiệu lực" in df.columns else "",
        notes=row["Ghi chú"] if "Ghi chú" in df.columns else ""
    )
    # Thực hiện chèn vào Neo4j
    graph.create(program_node)

print("Dữ liệu đã được chèn thành công vào Neo4j.")

