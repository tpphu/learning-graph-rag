from helper.openai import analyze_content_with_openai,save_to_yaml_file

# URL cần phân tích
url = "https://diemthi.tuyensinh247.com/de-an-tuyen-sinh/dai-hoc-y-duoc-can-tho-YCT.html"

# Gọi API để phân tích
yaml_result = analyze_content_with_openai(url)

# Lưu kết quả vào file nếu có dữ liệu
if yaml_result:
    save_to_yaml_file(yaml_result, "university_data_openai.yaml")
    print("Dữ liệu đã được lưu vào file 'university_data_openai.yaml'")
else:
    print("Không lấy được dữ liệu từ OpenAI API.")