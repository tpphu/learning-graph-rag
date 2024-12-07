import os

def save_to_file(yaml_content, file_path):
   with open(file_path, "w", encoding="utf-8") as yaml_file:
        yaml_file.write(yaml_content)
        
def load_file_content(file_path):
    """
    Kiểm tra nếu file tồn tại, load nội dung của file.
    
    Args:
        file_path (str): Đường dẫn tới file.
    
    Returns:
        str: Nội dung của file nếu tồn tại.
        None: Nếu file không tồn tại.
    """
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    else:
        print(f"File '{file_path}' không tồn tại.")
        return None