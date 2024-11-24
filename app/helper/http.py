import requests

def get_html_content(url):
    """
    Gửi yêu cầu GET đến một URL và trả về nội dung HTML.

    Args:
        url (str): Địa chỉ URL cần lấy nội dung HTML.

    Returns:
        str: Nội dung HTML dưới dạng chuỗi nếu yêu cầu thành công.
        None: Nếu yêu cầu thất bại.
    """
    try:
        # Gửi yêu cầu HTTP GET
        response = requests.get(url)
        # Kiểm tra mã trạng thái HTTP
        response.raise_for_status()  # Gây lỗi nếu mã trạng thái không phải 2xx
        
        # Đảm bảo mã hóa đúng
        response.encoding = response.apparent_encoding
        
        # Trả về nội dung HTML dưới dạng chuỗi
        return response.text
    except requests.exceptions.RequestException as e:
        # In lỗi và trả về None nếu có vấn đề xảy ra
        print(f"Error fetching URL {url}: {e}")
        return None
    
    
def get_text_content(url):
    """
    Gửi yêu cầu GET tới một URL, lấy nội dung HTML và trả về văn bản không chứa thẻ HTML.

    Args:
        url (str): Địa chỉ URL cần lấy nội dung văn bản.

    Returns:
        str: Văn bản không chứa thẻ HTML.
    """
    try:
        # Gửi yêu cầu HTTP GET
        response = requests.get(url)
        response.raise_for_status()  # Kiểm tra mã trạng thái HTTP
        response.encoding = response.apparent_encoding  # Thiết lập mã hóa phù hợp
        
        # Phân tích nội dung HTML với BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Loại bỏ các thẻ HTML, chỉ lấy nội dung văn bản
        text_content = soup.get_text(separator='\n').strip()
        
        return text_content
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        return None
    except Exception as e:
        print(f"Error processing HTML: {e}")
        return None
