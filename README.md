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



## Dữ liệu

https://vietnamnet.vn/giao-duc/diem-thi/tra-cuu-diem-chuan-cd-dh-2023/truong/dai-hoc-ba-ria-vung-tau?keyword=BVU


### Kết quả chạy:

```sh
root@1f21bd633e49:/app# pipenv  run python app/test_langchain.py
Loading .env environment variables...
Nodes:[Node(id='Quy Nhon University', type='Organization', properties={}), Node(id='Dqn', type='Identifier', properties={}), Node(id='Quy Nhon University English', type='Organization', properties={}), Node(id='Qnu', type='Identifier', properties={}), Node(id='170 An Duong Vuong, Tp. Quy Nhon, Binh Dinh', type='Location', properties={}), Node(id='Http://Www.Qnu.Edu.Vn', type='Website', properties={})]
Relationships:[Relationship(source=Node(id='Quy Nhon University', type='Organization', properties={}), target=Node(id='Dqn', type='Identifier', properties={}), type='IDENTIFIER', properties={}), Relationship(source=Node(id='Quy Nhon University', type='Organization', properties={}), target=Node(id='Quy Nhon University English', type='Organization', properties={}), type='ALTERNATE_NAME', properties={}), Relationship(source=Node(id='Quy Nhon University', type='Organization', properties={}), target=Node(id='Qnu', type='Identifier', properties={}), type='ALTERNATE_NAME', properties={}), Relationship(source=Node(id='Quy Nhon University', type='Organization', properties={}), target=Node(id='170 An Duong Vuong, Tp. Quy Nhon, Binh Dinh', type='Location', properties={}), type='LOCATION', properties={}), Relationship(source=Node(id='Quy Nhon University', type='Organization', properties={}), target=Node(id='Http://Www.Qnu.Edu.Vn', type='Website', properties={}), type='WEBSITE', properties={})]
```

```sh
Format lai:
Nodes:
[
    Node(id='Quy Nhon University', type='Organization', properties={}),
    Node(id='Dqn', type='Identifier', properties={}),
    Node(id='Quy Nhon University English', type='Organization', properties={}),
    Node(id='Qnu', type='Identifier', properties={}),
    Node(id='170 An Duong Vuong, Tp. Quy Nhon, Binh Dinh', type='Location', properties={}),
    Node(id='Http://Www.Qnu.Edu.Vn', type='Website', properties={})
]

Relationships:
[
    Relationship(
        source=Node(id='Quy Nhon University', type='Organization', properties={}),
        target=Node(id='Dqn', type='Identifier', properties={}),
        type='IDENTIFIER',
        properties={}
    ),
    Relationship(
        source=Node(id='Quy Nhon University', type='Organization', properties={}),
        target=Node(id='Quy Nhon University English', type='Organization', properties={}),
        type='ALTERNATE_NAME',
        properties={}
    ),
    Relationship(
        source=Node(id='Quy Nhon University', type='Organization', properties={}),
        target=Node(id='Qnu', type='Identifier', properties={}),
        type='ALTERNATE_NAME',
        properties={}
    ),
    Relationship(
        source=Node(id='Quy Nhon University', type='Organization', properties={}),
        target=Node(id='170 An Duong Vuong, Tp. Quy Nhon, Binh Dinh', type='Location', properties={}),
        type='LOCATION',
        properties={}
    ),
    Relationship(
        source=Node(id='Quy Nhon University', type='Organization', properties={}),
        target=Node(id='Http://Www.Qnu.Edu.Vn', type='Website', properties={}),
        type='WEBSITE',
        properties={}
    )
]
```


# Neo4j

https://python.langchain.com/docs/integrations/graphs/neo4j_cypher/