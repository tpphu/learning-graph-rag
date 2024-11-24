from openai import OpenAI

client = OpenAI()

def process_erd_file(file_path):
    # Đọc nội dung file tải lên
    with open(file_path, 'r') as file:
        file_content = file.read()

    # Prompt yêu cầu xử lý file
    prompt = f"""
    Dưới đây là nội dung của một file html về thông tin tuyển sinh:
    
    ```html
    {file_content}
    ```
    
    Hãy:
    1) Trích xuất toàn bộ nội dung liên quan đến ERD, bao gồm:
    - Danh sách các thực thể (entities) và các thuộc tính (attributes) của chúng.
    - Danh sách các mối quan hệ (relationships) giữa các thực thể.
    2) Giữ nguyên cấu trúc và trình bày dữ liệu dưới dạng YAML theo mẫu sau:
    yaml
    Thực thể:
      - Tên_thực_thể_1:
          Thuộc_tính:
            - Thuộc_tính_1: Giá trị
            - Thuộc_tính_2: Giá trị
      - Tên_thực_thể_2:
          Thuộc_tính:
            - Thuộc_tính_1: Giá trị
            - Thuộc_tính_2: Giá trị

    Mối quan hệ:
      - Quan_hệ_1:
          Thực_thể_liên_quan:
            - Tên_thực_thể_A
            - Tên_thực_thể_B
      - Quan_hệ_2:
          Thực_thể_liên_quan:
            - Tên_thực_thể_C
            - Tên_thực_thể_D

    3) Đảm bảo cấu trúc YAML hợp lệ, dễ đọc và giữ nguyên thứ tự các thực thể và mối quan hệ như trong file gốc.
    """

    # Gửi yêu cầu đến OpenAI API
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Bạn là một trợ lý phân tích tài liệu, giúp tôi đọc hiểu thông tin của một bài báo về tuyển sinh"},
            {"role": "user", "content": prompt}
        ],
        max_tokens=2000,
        temperature=0
    )

    # Trích xuất kết quả từ API
    yaml_data = response.choices[0].message.content

    # Lưu kết quả dưới dạng YAML
    output_file_path = "output_erd.yaml"
    with open(output_file_path, 'w') as output_file:
        output_file.write(yaml_data)

    print(f"Kết quả đã được lưu tại: {output_file_path}")
    return output_file_path

# Sử dụng hàm
file_path = "minified_page.html"  # Thay bằng đường dẫn thực tế
output_file = process_erd_file(file_path)
print(f"Tải xuống file đã xử lý tại: {output_file}")
