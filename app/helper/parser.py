import requests
import re
from bs4 import BeautifulSoup

def fetch_data_from_url(url):
    """
    Lấy dữ liệu từ một URL chứa các bảng HTML cụ thể.

    Args:
        url (str): Địa chỉ URL của trang web.

    Returns:
        list: Một danh sách các dictionary chứa dữ liệu từ bảng HTML.
    """
    try:
        # Gửi yêu cầu HTTP GET tới trang web
        response = requests.get(url)
        response.encoding = 'utf-8'  # Đảm bảo mã hóa đúng

        if response.status_code == 200:
            # Phân tích nội dung HTML của trang
            soup = BeautifulSoup(response.text, 'html.parser')

            # Tìm tất cả các bảng có cấu trúc cụ thể
            tables = soup.find_all('table', {
                'style': 'table-layout:auto'
            })
            
            titles = soup.find_all(class_="table__title")
            # Trích xuất văn bản từ từng phần tử
            titles_text = [title.get_text(strip=True) for title in titles]

            # Tạo danh sách để lưu trữ tất cả dữ liệu
            all_data = []
            idx = -1

            # Duyệt qua từng bảng tìm được
            for table in tables:
                rows = table.find_all('tr')
                idx = idx + 1
                admission_method = titles_text[idx].replace("Điểm chuẩn theo phương thức", "").replace("năm", " năm ")
                admission_method = admission_method.strip()
                admission_method = re.sub(r'\s+', ' ', admission_method)
                for row in rows[1:]:  # Bỏ qua hàng tiêu đề
                    cols = row.find_all('td')
                    cols = [ele.text.strip() for ele in cols]
                    if len(cols) == 6:  # Đảm bảo chỉ lấy các hàng có đủ 6 cột
                        all_data.append({
                            'Program Code': cols[1],
                            'Program Name': cols[2],
                            'Subject Combination': cols[3],
                            'Admission Score': cols[4],
                            'Admission method': admission_method,
                            'Note': cols[5],
                        })

            return all_data
        else:
            print(f"Yêu cầu không thành công. Mã trạng thái: {response.status_code}")
            return []
    except Exception as e:
        print(f"Lỗi khi xử lý URL {url}: {e}")
        return []