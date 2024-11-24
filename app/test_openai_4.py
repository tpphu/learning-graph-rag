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
    Phương thức xét tuyển: ĐT THPT
    Tên ngành: Kỹ thuật Y sinh
    Tổ hợp: B00
    Điểm chuẩn 2024: 22.8
  - Chỉ tiêu: 55
    Học phí: 33.1 triệu
    Mã ngành: '7520212'
    Phương thức xét tuyển: ĐT THPT
    Tên ngành: Kỹ thuật Y sinh
    Tổ hợp: A00
    Điểm chuẩn 2024: 22.1
  - Chỉ tiêu: 1035
    Học phí: 49.2 triệu
    Mã ngành: '7720101'
    Phương thức xét tuyển: ĐT THPT
    Tên ngành: Y khoa
    Tổ hợp: B00
    Điểm chuẩn 2024: 25.7
  - Chỉ tiêu: 150
    Học phí: 44.2 triệu
    Mã ngành: '7720110'
    Phương thức xét tuyển: ĐT THPT
    Tên ngành: Y học dự phòng
    Tổ hợp: B00
    Điểm chuẩn 2024: 22.7
  - Chỉ tiêu: 130
    Học phí: 44.2 triệu
    Mã ngành: '7720115'
    Phương thức xét tuyển: ĐT THPT
    Tên ngành: Y học cổ truyền
    Tổ hợp: B00
    Điểm chuẩn 2024: 24.48
  - Chỉ tiêu: 200
    Học phí: 49.7 triệu
    Mã ngành: '7720201'
    Phương thức xét tuyển: ĐT THPT
    Tên ngành: Dược học
    Tổ hợp: B00
    Điểm chuẩn 2024: 24.78
  - Chỉ tiêu: 105
    Học phí: 38.6 triệu
    Mã ngành: '7720301'
    Phương thức xét tuyển: ĐT THPT
    Tên ngành: Điều dưỡng
    Tổ hợp: B00
    Điểm chuẩn 2024: 23.45
  - Chỉ tiêu: 50
    Học phí: 33.1 triệu
    Mã ngành: '7720302'
    Phương thức xét tuyển: ĐT THPT
    Tên ngành: Hộ sinh
    Tổ hợp: B00
    Điểm chuẩn 2024: 22.35
  - Chỉ tiêu: 150
    Học phí: 49.2 triệu
    Mã ngành: '7720501'
    Phương thức xét tuyển: ĐT THPT
    Tên ngành: Răng hàm mặt
    Tổ hợp: B00
    Điểm chuẩn 2024: 25.65
  - Chỉ tiêu: 100
    Học phí: 38.6 triệu
    Mã ngành: '7720601'
    Phương thức xét tuyển: ĐT THPT
    Tên ngành: Kỹ thuật Xét nghiệm y học
    Tổ hợp: B00
    Điểm chuẩn 2024: 24.38
  - Chỉ tiêu: 50
    Học phí: 33.1 triệu
    Mã ngành: '7720602'
    Phương thức xét tuyển: ĐT THPT
    Tên ngành: Kỹ thuật Hình ảnh y học
    Tổ hợp: B00
    Điểm chuẩn 2024: 23.75
  - Chỉ tiêu: 40
    Học phí: 33.1 triệu
    Mã ngành: '7720701'
    Phương thức xét tuyển: ĐT THPT
    Tên ngành: Y tế công cộng
    Tổ hợp: B00
    Điểm chuẩn 2024: 19.2
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
        max_tokens=2000,
        temperature=0
    )

    # Trích xuất kết quả từ API
    yaml_data = response.choices[0].message.content

    # Lưu kết quả dưới dạng YAML
    output_file_path = "dai-hoc-bach-khoa-dai-hoc-quoc-gia-tphcm-QSB.yaml"
    with open(output_file_path, 'w') as output_file:
        output_file.write(yaml_data)

    print(f"Kết quả đã được lưu tại: {output_file_path}")
    return output_file_path

# Sử dụng hàm
file_path = "dai-hoc-bach-khoa-dai-hoc-quoc-gia-tphcm-QSB.html"  # Thay bằng đường dẫn thực tế
output_file = process_erd_file(file_path)
print(f"Tải xuống file đã xử lý tại: {output_file}")
