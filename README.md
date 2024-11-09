# GraphRAG


# Import danh sach truong dai hoc

## Import danh sach vao neo4j

```sh
docker-compose up -d neo4j
docker-compose run -it shell
pipenv run python ./app/import_training_programs_university.py
```

## Xem danh sach cac node

> http://localhost:7474/browser/
> 
> neo4j/password


```cyber
MATCH (n) RETURN n LIMIT 100;
MATCH (n) RETURN COUNT(n);
```

## Nhận diện thực thể sử dụng ChatGPT

Ví dụ: https://vnexpress.net/co-hoi-xet-tuyen-truong-quoc-te-dh-quoc-gia-ha-noi-tu-20-diem-4784076.html

Dữ liệu:

! ./entities_relationships.yaml


