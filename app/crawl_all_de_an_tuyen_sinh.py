import os
import pandas as pd

from helper.openai import export_erd_from_html
from helper.http import WebDriverManager, fetch_and_minify_html
from helper.file import save_to_file, load_file_content


if __name__ == "__main__":
    # Đọc nội dung file CSV ve truong dai hoc
    file_path = 'university_links.csv'
    data = pd.read_csv(file_path)

    # Khởi tạo WebDriver
    driver_manager = WebDriverManager()  

    try:
        for index, row in data.iterrows():
            path = row['Liên kết'].replace('/diem-chuan/', '')
            
            # Step 1 - Crawl noi dung - kiem tra neu da ton tai file html thi khong crawl nua
            url = 'https://diemthi.tuyensinh247.com/de-an-tuyen-sinh/%s' % path
            print("Dang crawl url:", url)
            html_file_path = "input/%s" % (path)
            minify_html_content = load_file_content(html_file_path)
            if minify_html_content is None:
                minify_html_content = fetch_and_minify_html(url, driver_manager.driver)
            if minify_html_content:
                save_to_file(minify_html_content, html_file_path)
                print("HTML content-length: ", len(minify_html_content))
            else:
                print("Can not download html")
                continue
            # Step 2 - Goi Open AI de trich xuat ERD, neu ton tai file thi khong goi nua de tiet kiem chi phi
            yaml_file_path = 'output/'+path.replace('.html', '.yaml')
            if os.path.exists(yaml_file_path):
                print("Da ton tai file: %s" % (yaml_file_path))
                continue
            # Step 2.1 - Goi len OpenAI de lay ERD
            yaml_result = export_erd_from_html(minify_html_content)
            # Lưu kết quả vào file nếu có dữ liệu
            if yaml_result:
                save_to_file(yaml_result, yaml_file_path)
                print("Dữ liệu ERD đã được lưu vào file %s" % (yaml_file_path))
            else:
                print("Không lấy được dữ liệu từ OpenAI API.")
    finally:     
        driver_manager.close()
