from openai import OpenAI

client = OpenAI()

def generate_yaml_with_openai(prompt):
    """
    Sử dụng OpenAI API để tạo dữ liệu YAML từ prompt.
    """
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Bạn là một trợ lý hữu ích."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=2000,
        temperature=0
    )
    return response.choices[0].message.content

def save_yaml_file(data, filename):
    """
    Lưu dữ liệu vào tệp YAML.
    """
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(data)

if __name__ == "__main__":
    url = "https://diemthi.tuyensinh247.com/de-an-tuyen-sinh/dai-hoc-y-duoc-can-tho-YCT.html"
    try:
        # Tạo prompt cho OpenAI
        prompt = f"""
        Dưới đây là một đường dẫn url được cung cấp. Hãy trích xuất thông tin dưới dạng YAML với các tiêu chí sau:
        
        - Tên trường đại học.
        - Ngành đào tạo: Tên ngành, mã ngành, chỉ tiêu, hệ đào tạo, học phí.
        - Phương thức xét tuyển: Tên phương thức, ngưỡng điểm, tổ hợp xét tuyển.
        - Các mối quan hệ giữa ngành đào tạo, phương thức xét tuyển, và học phí.

        Đường dẫn (url) trang web:
        {url}

        Trả kết quả dưới dạng YAML, có format ví dụ như sau:
        
        ```yaml
        entities:
        - name: "Trường Đại học Y Dược Cần Thơ"
            type: "University"
            attributes:
            address: "179 Nguyễn Văn Cừ, phường An Khánh, quận Ninh Kiều, thành phố Cần Thơ"
            website: "https://www.ctump.edu.vn/"
            facebook: "http://facebook.com/dhydct.ctump/edu/vn"
            contact_year: 2024

        - name: "Phương thức tuyển sinh"
            type: "Admission Methods"
            attributes:
            methods:
                - name: "Xét tuyển dựa trên kết quả Kỳ thi tốt nghiệp THPT"
                description: "Xét tuyển tổ hợp môn Toán, Hóa, Sinh"
                - name: "Xét tuyển thẳng và ưu tiên xét tuyển"
                description: "Theo quy định của Bộ Giáo dục và Đào tạo"

        - name: "Chỉ tiêu tuyển sinh"
            type: "Admission Quotas"
            attributes:
            total: 2260
            year: 2024

        - name: "Ngành đào tạo"
            type: "Programs"
            attributes:
            programs:
                - name: "Y khoa, Răng Hàm Mặt"
                tuition_fee: 49150000
                - name: "Dược học"
                tuition_fee: 49685000
                - name: "Y học cổ truyền, Y học dự phòng"
                tuition_fee: 44152000
                - name: "Điều dưỡng, Kỹ thuật xét nghiệm y học"
                tuition_fee: 38645000
                - name: "Kỹ thuật Hình ảnh y học, Hộ sinh, Y tế công cộng"
                tuition_fee: 33110000

        - name: "Điểm chuẩn năm 2024"
            type: "Admission Scores"
            attributes:
            publish_date: "17/08/2024"
            details_link: "https://diemthi.tuyensinh247.com/diem-chuan/dai-hoc-y-duoc-can-tho-YCT.html"

        relationships:
        - source: "Trường Đại học Y Dược Cần Thơ"
            target: "Phương thức tuyển sinh"
            type: "offers"

        - source: "Trường Đại học Y Dược Cần Thơ"
            target: "Chỉ tiêu tuyển sinh"
            type: "has"

        - source: "Trường Đại học Y Dược Cần Thơ"
            target: "Ngành đào tạo"
            type: "provides"

        - source: "Trường Đại học Y Dược Cần Thơ"
            target: "Điểm chuẩn năm 2024"
            type: "publishes"

        ```
        """
        
        # Sử dụng OpenAI để tạo dữ liệu YAML
        yaml_data = generate_yaml_with_openai(prompt)
        
        # Lưu dữ liệu vào tệp YAML
        file = "university_data_3.yaml"
        save_yaml_file(yaml_data, file)
        
        print("Dữ liệu đã được trích xuất và lưu vào '%s'" % file)
    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")
