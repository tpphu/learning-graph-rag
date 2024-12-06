from openai import OpenAI

client = OpenAI()

def process_erd_file(file_path):
    # Đọc nội dung file tải lên
    with open(file_path, 'r') as file:
        file_content = file.read()

    # Prompt yêu cầu xử lý file
    prompt = f"""
    Dưới đây là nội dung của một file định dạng html về thông tin tuyển sinh:
    
    ```html
    {file_content}
    ```
    
    Hãy:

    1) Trích xuất toàn bộ nội dung liên quan đến ERD, bao gồm:
    - Danh sách các thực thể (entities) và các thuộc tính (attributes) của chúng.
    - Danh sách các mối quan hệ (relationships) giữa các thực thể.

    2) Giữ nguyên cấu trúc và trình bày dữ liệu dưới dạng YAML theo một mẫu ví dụ sau:

```yaml
Mối quan hệ:
- Ngành đào tạo: Tất cả các ngành
  Trường: Trường Đại học Y Dược Cần Thơ
- Ngành đào tạo: Tất cả các ngành
  Phương thức xét tuyển: ĐT THPT
- Ngành đào tạo: Tất cả các ngành
  Tổ hợp:
  - B00
  - A00
- Trường: Trường Đại học Y Dược Cần Thơ
  Địa chỉ: 179 Nguyễn Văn Cừ, phường An Khánh, quận Ninh Kiều, thành phố Cần Thơ
Thực thể:
  Ngành đào tạo:
  - Chỉ tiêu: 55
    Học phí: 33.1 triệu
    Mã ngành: '7520212'
    Tên ngành: Kỹ thuật Y sinh
    Phương thức xét tuyển:
      - Loại: ĐT THPT
        Tổ hợp: B00
        Điểm chuẩn 2024: 22.1
  - Chỉ tiêu: 55
    Học phí: 33.1 triệu
    Mã ngành: '7140247'
    Tên ngành: Sư phạm Khoa học tự nhiên
    Phương thức xét tuyển:
      - Loại: ĐT THPT
        Tổ hợp: A00
        Điểm chuẩn 2024: 22.1
      - Loại: ĐGNL SPHN
        Tổ hợp: N/A
        Điểm chuẩn 2024: 22.5
      - Loại: Học Bạ
        Tổ hợp: A00; A01; A02; B00
        Điểm chuẩn 2024: 28.5
  Trường Đại học:
    Facebook: http://facebook.com/dhydct.ctump/edu/vn
    Mã trường: YCT
    Tên: Trường Đại học Y Dược Cần Thơ
    Website: https://www.ctump.edu.vn/
    Địa chỉ: 179 Nguyễn Văn Cừ, phường An Khánh, quận Ninh Kiều, thành phố Cần Thơ
```

    3) Đảm bảo cấu trúc YAML hợp lệ, dễ đọc và giữ nguyên thứ tự các thực thể và mối quan hệ như trong file gốc.
    """

    # Gửi yêu cầu đến OpenAI API
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Bạn là một trợ lý phân tích tài liệu, giúp tôi đọc hiểu thông tin của một bài báo về tuyển sinh"},
            {"role": "user", "content": prompt}
        ],
        max_tokens=4000,
        temperature=0
    )

    # Trích xuất kết quả từ API
    yaml_data = response.choices[0].message.content

    # Lưu kết quả dưới dạng YAML
    output_file_path = "dai-hoc-quy-nhon-DQN.yaml"
    with open(output_file_path, 'w') as output_file:
        output_file.write(yaml_data)

    print(f"Kết quả đã được lưu tại: {output_file_path}")
    return output_file_path

# Sử dụng hàm
file_path = "dai-hoc-quy-nhon-DQN.html"  # Thay bằng đường dẫn thực tế
output_file = process_erd_file(file_path)
print(f"Tải xuống file đã xử lý tại: {output_file}")
