import pandas as pd
import time
import mysql.connector
from helper.parser import fetch_data_from_url

def connect_to_db():
    return mysql.connector.connect(
        host="mysql", 
        user="root",
        password="root",
        database="university_db"
    )
    
# Tạo bảng nếu chưa tồn tại
def create_table_if_not_exists(cursor):
    create_table_query = """
    CREATE TABLE IF NOT EXISTS university_scores (
        id INT AUTO_INCREMENT PRIMARY KEY,
        university_name VARCHAR(2048),
        program_code VARCHAR(255),
        program_name VARCHAR(255),
        subject_combination VARCHAR(255),
        admission_score FLOAT,
        note TEXT
    )
    """
    cursor.execute(create_table_query)
    
def save_to_db(university_name, data, connection):
    cursor = connection.cursor()
    insert_query = """
    INSERT INTO university_scores (university_name, program_code, program_name, subject_combination, admission_score, note)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    for row in data:
        cursor.execute(insert_query, (
            university_name,
            row['Program Code'], 
            row['Program Name'], 
            row['Subject Combination'], 
            float(row['Admission Score']) if row['Admission Score'] else None, 
            row['Note']
        ))
    connection.commit()
    
# Đọc nội dung file CSV
file_path = 'university_links.csv'
data = pd.read_csv(file_path)

connection = connect_to_db()
create_table_if_not_exists(connection.cursor())

for index, row in data.iterrows():
    url = 'https://diemthi.tuyensinh247.com%s' % row['Liên kết']
    university_name = row['Tên trường']
    print("Dang crawl url:", url)
    data = fetch_data_from_url(url)
    print(university_name, " | so record: ",len(data))
    save_to_db(university_name, data, connection)
    # Sleep moi giay de tranh block
    time.sleep(3)
