import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL của trang web cần thu thập dữ liệu
url = 'https://diemthi.tuyensinh247.com/diem-chuan/dai-hoc-thu-do-ha-noi-HNM.html'

# Gửi yêu cầu HTTP GET tới trang web
response = requests.get(url)
response.encoding = 'utf-8'  # Đảm bảo mã hóa đúng

# Kiểm tra xem yêu cầu có thành công không
if response.status_code == 200:
    # Phân tích nội dung HTML của trang
    soup = BeautifulSoup(response.text, 'html.parser')

    # Tìm tất cả các bảng có cấu trúc cụ thể
    tables = soup.find_all('table', {
        'width': '100%',
        'border': '0',
        'cellpadding': '0',
        'cellspacing': '0'
    })

    # Tạo danh sách để lưu trữ tất cả dữ liệu
    all_data = []

    # Duyệt qua từng bảng tìm được
    for table in tables:
        print(f'Tim thay table')
        rows = table.find_all('tr')
        for row in rows[1:]:  # Bỏ qua hàng tiêu đề
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            if len(cols) == 6:
                all_data.append({
                    'Mã ngành': cols[1],
                    'Tên ngành': cols[2],
                    'Tổ hợp môn': cols[3],
                    'Điểm chuẩn': cols[4],
                    'Ghi chú': cols[5]
                })

    # Chuyển dữ liệu thành DataFrame
    df = pd.DataFrame(all_data)

    # Lưu dữ liệu vào file CSV
    output_csv = 'diem_chuan_dai_hoc_thu_do_ha_noi_all_tables.csv'
    df.to_csv(output_csv, index=False, encoding='utf-8-sig')
    print(f'Dữ liệu đã được lưu vào file {output_csv}')

else:
    print(f'Yêu cầu không thành công. Mã trạng thái: {response.status_code}')
