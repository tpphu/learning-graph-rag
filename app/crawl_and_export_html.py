from helper.http import fetch_and_minify_html

if __name__ == "__main__":
    url = "https://diemthi.tuyensinh247.com/de-an-tuyen-sinh/dai-hoc-quy-nhon-DQN.html"
    minified_html = fetch_and_minify_html(url)

    # Lưu nội dung sạch vào file
    with open("dai-hoc-quy-nhon-DQN.html", "w", encoding="utf-8") as f:
        f.write(minified_html)
    print("Minified HTML content saved to minified_page.html")
