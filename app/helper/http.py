import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import re

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

def fetch_and_minify_html(url, wait_time=5):
    """
    Fetches the full HTML content of a web page, removes unnecessary elements, attributes, and minifies the result.
    """
    # Thiết lập Chrome headless
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Chế độ không giao diện
    chrome_options.add_argument("--no-sandbox")  # Bỏ sandbox để phù hợp Docker
    chrome_options.add_argument("--disable-dev-shm-usage")  # Xử lý chia sẻ bộ nhớ
    chrome_options.add_argument("--disable-gpu")  # Không cần GPU trong Docker
    chrome_options.add_argument("--window-size=1920x1080")  # Đặt kích thước cửa sổ

    # Khởi tạo WebDriver
    service = Service('/usr/local/bin/chromedriver')  # Đường dẫn Chromedriver
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Mở URL
        driver.get(url)
        
        # Chờ một khoảng thời gian để đảm bảo nội dung tải xong
        time.sleep(wait_time)

        # Lấy toàn bộ mã HTML đầy đủ
        full_html = driver.page_source

        # Làm sạch HTML bằng BeautifulSoup
        soup = BeautifulSoup(full_html, "html.parser")

        # Loại bỏ các thẻ <script>, <style>, <svg> và các thẻ không mong muốn khác
        for tag in soup(["script", "style", "svg", "iframe", "meta"]):
            tag.decompose()

        # Loại bỏ tất cả attributes của các thẻ còn lại
        for tag in soup.find_all(True):  # Lấy tất cả các thẻ HTML
            tag.attrs = {}  # Xóa attributes

        # Tối ưu HTML: loại bỏ khoảng trắng và xuống dòng không cần thiết
        minified_html = re.sub(r">\s+<", "><", str(soup))  # Loại bỏ khoảng trắng giữa các thẻ
        minified_html = re.sub(r"\s+", " ", minified_html).strip()  # Loại bỏ khoảng trắng thừa

        # Trả về nội dung sạch và tối ưu
        return minified_html
    finally:
        # Đóng WebDriver
        driver.quit()