import requests
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

            # Tạo danh sách để lưu trữ tất cả dữ liệu
            all_data = []

            # Duyệt qua từng bảng tìm được
            for table in tables:
                rows = table.find_all('tr')
                for row in rows[1:]:  # Bỏ qua hàng tiêu đề
                    cols = row.find_all('td')
                    cols = [ele.text.strip() for ele in cols]
                    if len(cols) == 6:  # Đảm bảo chỉ lấy các hàng có đủ 6 cột
                        all_data.append({
                            'Program Code': cols[1],
                            'Program Name': cols[2],
                            'Subject Combination': cols[3],
                            'Admission Score': cols[4],
                            'Note': cols[5]
                        })

            return all_data
        else:
            print(f"Yêu cầu không thành công. Mã trạng thái: {response.status_code}")
            return []
    except Exception as e:
        print(f"Lỗi khi xử lý URL {url}: {e}")
        return []