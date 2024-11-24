import openai

client = OpenAI()

def analyze_content_with_openai(url):
    """
    Gọi OpenAI API để phân tích nội dung từ URL và chuyển đổi thành YAML.

    Args:
        url (str): Đường dẫn URL cần phân tích.

    Returns:
        str: Dữ liệu phân tích ở dạng YAML.
    """
    # Prompt để gửi tới OpenAI
    prompt = f"""
    Phân tích nội dung từ URL sau: {url}.
    Trích xuất thông tin và chuyển đổi thành các thực thể (entities) và các mối quan hệ (relationships) dưới dạng YAML.
    Các thực thể có thể bao gồm:
    - Tên trường đại học
    - Phương thức tuyển sinh
    - Chỉ tiêu tuyển sinh
    - Ngành đào tạo
    - Điểm chuẩn
    Các mối quan hệ bao gồm kết nối giữa các thực thể, ví dụ như "offers", "provides".
    """
    try:
        # Gọi OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates YAML data structures."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0
        )
        
        # Lấy kết quả trả về
        result = response['choices'][0]['message']['content']
        return result
    except Exception as e:
        print(f"Error while calling OpenAI API: {e}")
        return None

def save_to_yaml_file(yaml_content, file_path):
    """
    Lưu nội dung YAML vào file.

    Args:
        yaml_content (str): Nội dung YAML.
        file_path (str): Đường dẫn file.
    """
    with open(file_path, "w", encoding="utf-8") as yaml_file:
        yaml_file.write(yaml_content)

