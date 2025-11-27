### docker 실행 방법 (db만)

```bash
docker run -d --name check-db -p 3306:3306 seoyoon954/sookmissing_db:v1
```

### docker 테스트 방법 (db 잘 들어왔는지)
```bash
docker exec -it check-db mysql -u root -p1234

USE sookmissing_db;
SELECT COUNT(*) FROM bad_urls;
```

<img width="483" height="190" alt="image" src="https://github.com/user-attachments/assets/f656725d-7ef3-431d-9edc-7287ea0b08da" />
<br/>
이렇게 나오면 잘 된겁니다~~
