from openai import OpenAI
import requests
from bs4 import BeautifulSoup

client = OpenAI()

def fetch_web_content(url):
    """
    Lấy nội dung HTML từ trang web.
    """
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Không thể lấy nội dung từ {url}, mã trạng thái: {response.status_code}")

def extract_text_from_html(html_content):
    """
    Trích xuất văn bản thuần từ nội dung HTML.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup.get_text(separator='\n')

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
        # Lấy nội dung từ trang web
        html_content = fetch_web_content(url)
        
        # Trích xuất văn bản thuần từ HTML
        plain_text = extract_text_from_html(html_content)
        
        # Tạo prompt cho OpenAI
        prompt = f"""
        Dưới đây là nội dung trang web được cung cấp. Hãy trích xuất thông tin dưới dạng YAML với các tiêu chí sau:
        
        - Tên trường đại học.
        - Ngành đào tạo: Tên ngành, mã ngành, chỉ tiêu, hệ đào tạo, học phí.
        - Phương thức xét tuyển: Tên phương thức, ngưỡng điểm, tổ hợp xét tuyển.
        - Các mối quan hệ giữa ngành đào tạo, phương thức xét tuyển, và học phí.

        Nội dung trang web:
        {plain_text}

        Trả kết quả dưới dạng YAML:
        """
        
        # Sử dụng OpenAI để tạo dữ liệu YAML
        yaml_data = generate_yaml_with_openai(prompt)
        
        # Lưu dữ liệu vào tệp YAML
        save_yaml_file(yaml_data, "university_data.yaml")
        
        print("Dữ liệu đã được trích xuất và lưu vào 'university_data.yaml'")
    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")
