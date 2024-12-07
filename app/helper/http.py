import re
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
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
    def __init__(self, driver_path='/usr/local/bin/chromedriver'):
        self.driver_path = driver_path
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.chrome_options.add_argument("--disable-gpu")
        self.chrome_options.add_argument("--window-size=1920x1080")
        self.driver = None

    def get_driver(self):
        # Khởi tạo lại driver nếu cần
        if self.driver is None:
            self.driver = webdriver.Chrome(service=Service(self.driver_path), options=self.chrome_options)
        return self.driver

    def reset_driver(self):
        # Đóng và khởi tạo lại driver
        if self.driver:
            self.driver.quit()
        self.driver = webdriver.Chrome(service=Service(self.driver_path), options=self.chrome_options)

    def close_driver(self):
        if self.driver:
            self.driver.quit()
            self.driver = None

def fetch_and_minify_html(url, driver_manager, timeout=10):
    """
    Fetches and minifies HTML content using Selenium and BeautifulSoup.
    """
    driver = driver_manager.get_driver()
    try:
        # Thiết lập timeout cho driver
        driver.set_page_load_timeout(timeout)

        # Mở URL
        driver.get(url)
        print(f"Opening {url}...")

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
    except (TimeoutException, WebDriverException) as e:
        print(f"Error fetching {url}: {e}. Resetting driver...")
        driver_manager.reset_driver()  # Khởi tạo lại driver
        return None