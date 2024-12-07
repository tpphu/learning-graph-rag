import pandas as pd

from helper.openai import export_erd_from_html
from helper.http import fetch_and_minify_html
from helper.file import save_to_file, load_file_content

# Đọc nội dung file CSV
file_path = 'university_links.csv'
data = pd.read_csv(file_path)


for index, row in data.iterrows():
    path = row['Liên kết'].replace('/diem-chuan/', '')
    url = 'https://diemthi.tuyensinh247.com/de-an-tuyen-sinh/%s' % path
    print("Dang crawl url:", url)
    html_file_path = "input/%s" % (path)
    minify_html_content = load_file_content(html_file_path)
    if minify_html_content is None:
        minify_html_content = fetch_and_minify_html(url)
        save_to_file(minify_html_content, html_file_path)
    if minify_html_content:
        print("HTML content-length: ", len(minify_html_content))
    yaml_result = export_erd_from_html(minify_html_content)

    # Lưu kết quả vào file nếu có dữ liệu
    if yaml_result:
        yaml_file_path = 'output/'+path.replace('.html', '.yaml')
        save_to_file(yaml_result, yaml_file_path)
        print("Dữ liệu đã được lưu vào file %s" % (yaml_file_path))
    else:
        print("Không lấy được dữ liệu từ OpenAI API.")
