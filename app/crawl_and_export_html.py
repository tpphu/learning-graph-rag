from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import re

def fetch_and_minify_html(url, wait_time=10):
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

if __name__ == "__main__":
    url = "https://diemthi.tuyensinh247.com/de-an-tuyen-sinh/dai-hoc-y-duoc-can-tho-YCT.html"
    minified_html = fetch_and_minify_html(url)

    # Lưu nội dung sạch vào file
    with open("minified_page.html", "w", encoding="utf-8") as f:
        f.write(minified_html)
    print("Minified HTML content saved to minified_page.html")
