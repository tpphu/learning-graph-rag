import re
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup


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

class WebDriverManager:
    """
    Quản lý WebDriver để tái sử dụng trình duyệt.
    """
    def __init__(self, driver_path='/usr/local/bin/chromedriver'):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920x1080")
        self.driver = webdriver.Chrome(service=Service(driver_path), options=chrome_options)

    def close(self):
        self.driver.quit()

def fetch_and_minify_html(url, driver, wait_time=5):
    """
    Fetches and minifies HTML content using Selenium and BeautifulSoup.
    """
    try:
        # Mở URL
        driver.get(url)
        print(f"Opening {url}...")

        # Chờ đến khi trang tải xong
        WebDriverWait(driver, wait_time).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # Lấy HTML đầy đủ
        full_html = driver.page_source

        # Làm sạch HTML bằng BeautifulSoup
        soup = BeautifulSoup(full_html, "html.parser")

        # Loại bỏ các thẻ không cần thiết
        for tag in soup(["script", "style", "svg", "iframe", "meta"]):
            tag.decompose()

        # Loại bỏ tất cả attributes
        for tag in soup.find_all(True):
            tag.attrs = {}

        # Minify HTML
        minified_html = re.sub(r">\s+<", "><", str(soup)).strip()

        return minified_html
    except Exception as e:
        print(f"Error fetching HTML from {url}: {e}")
        return None