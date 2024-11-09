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
> neo4j/password


```cyber
    MATCH (n) RETURN n LIMIT 100;
MATCH (n) RETURN COUNT(n);
```


