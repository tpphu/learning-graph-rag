import spacy

# Tải mô hình ngôn ngữ (ở đây sử dụng tiếng Anh)
nlp = spacy.load("en_core_web_sm")

# Đoạn văn bản để nhận diện thực thể
text = "Anh An đang đọc cuốn sách Lược sử loài người của Yuval Noah Harari"

# Sử dụng spaCy để phân tích câu
doc = nlp(text)

# Tạo danh sách các thực thể
entities = []
for ent in doc.ents:
    entities.append({
        "text": ent.text,
        "type": ent.label_
    })

# Định dạng kết quả dưới dạng JSON
import json
result = json.dumps({"entities": entities}, indent=2, ensure_ascii=False)
print(result)

