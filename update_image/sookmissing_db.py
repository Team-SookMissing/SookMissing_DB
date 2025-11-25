import requests
import pymysql
import os

try :
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# API 정보
api_url = "https://api.odcloud.kr/api/15143094/v1/uddi:083f29fd-a18a-4c23-81e5-8aa5101c4ac6"
api_key = os.getenv("API_KEY")

# DB 연결 정보
DB_CONFIG = {
    'host': os.getenv('DB_HOST', '127.0.0.1'), 
    'port': 3306,
    'user': 'root',
    'password': os.getenv("DB_PASSWORD", "1234"),
    'db': 'sookmissing_db',
    'charset': 'utf8mb4'
}

def main():
    conn = None
    try:
        conn = pymysql.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # 테이블 생성 (없으면 자동 생성, UNIQUE 문제 해결)
        create_table = """
        CREATE TABLE IF NOT EXISTS bad_urls (
            id INT AUTO_INCREMENT PRIMARY KEY,
            url VARCHAR(2083) NOT NULL,
            source_date VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE KEY unique_url (url(255))
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """
        cursor.execute(create_table)
        print("Table ready")

        # 전체 페이지 반복해서 데이터 가져오기
        page = 1
        per_page = 100
        total_inserted = 0

        while True:
            params = {
                'serviceKey': api_key,
                'page': page,
                'perPage': per_page,
                'returnType': 'JSON'
            }

            response = requests.get(api_url, params=params)
            if response.status_code != 200:
                print(f"Error {response.status_code}")
                print(response.text)
                break

            data = response.json()
            items = data.get('data', [])

            if not items:
                print("No more data to fetch.")
                break

            inserted_cnt = 0
            for item in items:
                url = item.get('홈페이지주소')
                date = item.get('날짜')
                if url:
                    insert_query = """
                    INSERT IGNORE INTO bad_urls (url, source_date)
                    VALUES (%s, %s);
                    """
                    cursor.execute(insert_query, (url, date))
                    if cursor.rowcount > 0:
                        inserted_cnt += 1
                        total_inserted += 1

            print(f"Page {page} processed, {len(items)} items fetched, {inserted_cnt} new inserted.")
            page += 1

        conn.commit()
        print(f"Total {total_inserted} new URLs inserted into the database.")

    except Exception as e:
        print("Error:", e)

    finally:
        if conn:
            conn.close()
            print("DB connection closed.")

if __name__ == "__main__":
    main()
