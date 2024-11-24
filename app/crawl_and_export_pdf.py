from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import base64
import os
import time

def fetch_and_save_as_pdf(url, output_file, wait_time=10):
    """
    Fetches dynamic content from a web page in headless mode and exports it as a PDF.
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
        
        # Chờ một khoảng thời gian để nội dung tải xong
        time.sleep(wait_time)
        
        # Đảm bảo nội dung trang được xử lý với UTF-8
        driver.page_source.encode("utf-8")  # Lấy nội dung trang mã hóa UTF-8
        
        # Tạo PDF
        pdf_options = {
            "landscape": False,
            "displayHeaderFooter": False,
            "printBackground": True,
            "paperWidth": 11,  # Inches (8.5 x 11 là khổ A4)
            "paperHeight": 8.5,
            "marginTop": 0.25,
            "marginBottom": 0.25,
            "marginLeft": 0.25,
            "marginRight": 0.25
        }

        # Sử dụng DevTools Protocol để xuất PDF
        pdf_data = driver.execute_cdp_cmd("Page.printToPDF", pdf_options)

        # Decode Base64 PDF content and save it to a file
        pdf_path = os.path.abspath(output_file)
        with open(pdf_path, "wb") as pdf_file:
            pdf_file.write(base64.b64decode(pdf_data["data"]))
        
        print(f"PDF saved to: {pdf_path}")
    finally:
        # Đóng WebDriver
        driver.quit()

if __name__ == "__main__":
    url = "https://diemthi.tuyensinh247.com/de-an-tuyen-sinh/dai-hoc-y-duoc-can-tho-YCT.html"
    output_file = "output.pdf"
    fetch_and_save_as_pdf(url, output_file)
