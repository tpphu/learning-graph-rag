from py2neo import Graph, Node
import pandas as pd

# Kết nối tới cơ sở dữ liệu Neo4j
graph = Graph("bolt://neo4j:7687", auth=("neo4j", "password"))

# Đọc dữ liệu từ file CSV
csv_file_path = "diem_chuan_dai_hoc_thu_do_ha_noi_all_tables.csv"
df = pd.read_csv(csv_file_path)

# Thay thế giá trị NaN bằng chuỗi rỗng
df = df.fillna("")

# Chèn dữ liệu vào Neo4j
for index, row in df.iterrows():
    # Tạo Node cho ngành đào tạo (UniversityProgram)
    program_node = Node(
        "UniversityProgram",
        code=row['Mã ngành'],
        name=row['Tên ngành']
    )
    graph.merge(program_node, "UniversityProgram", "code")

    # Tạo Node cho tổ hợp môn (SubjectCombination)
    subject_combination_node = Node(
        "SubjectCombination",
        combination=row['Tổ hợp môn']
    )
    graph.merge(subject_combination_node, "SubjectCombination", "combination")

    # Tạo quan hệ "HAS_SCORE" giữa UniversityProgram và SubjectCombination
    graph.run(
        """
        MATCH (p:UniversityProgram {code: $code}), (s:SubjectCombination {combination: $combination})
        MERGE (p)-[:HAS_SCORE {score: $score, note: $note}]->(s)
        """,
        code=row['Mã ngành'],
        combination=row['Tổ hợp môn'],
        score=row['Điểm chuẩn'],
        note=row['Ghi chú']
    )

print("Dữ liệu đã được chèn thành công vào Neo4j.")
