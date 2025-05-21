from requests_html import HTMLSession
import re
import mysql.connector

def connect_to_database():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='1234',
            database='mysql',
            port=3306
        )
        if conn.is_connected():
            print("Successfully connected to the database")
            return conn
        else:
            print("Failed to connect")
            return None
    except mysql.connector.Error as e:
        print(f"Database connection failed: {e}")
        return None

def getLast_id(conn):
    # SQL 쿼리를 정의합니다.
    query = """
    SELECT MAX(siteId) FROM PerformancesInfo
    WHERE site = 'yes24'
    """

    # 커서를 생성하고 쿼리를 실행합니다.
    cursor = conn.cursor()
    cursor.execute(query)

    # 결과를 가져옵니다. 결과가 없을 경우 None을 반환할 것입니다.
    max_id = cursor.fetchone()[0]

    # 커서와 연결을 정리합니다.
    cursor.close()

    # 최대 siteId를 반환합니다.
    return max_id


def scrape_and_insert_data(conn, last_id, base_url='http://ticket.yes24.com/New/Notice/NoticeMain.aspx', page_number=1):
    session = HTMLSession()
    url = f"{base_url}?#page={page_number}"
    url2 = ""

    try:
        r = session.get(url)
        r.html.render()  # JavaScript 렌더링을 위해 호출

        rows = r.html.find('#BoardList tr')
        cursor = conn.cursor()
        continue_scraping = True

        for row in rows[1:]:  # 첫 번째 행 제외
            cells = row.find('td')
            if len(cells) >= 3:
                second_cell = cells[1].text  # 공연명
                third_cell = cells[2].text  # 날짜
                a_tag = cells[1].find('a', first=True)

                if a_tag:
                    href = a_tag.attrs.get('href', '')
                    db_url = base_url + href
                    id_match = re.search(r'id=(\d+)', href)
                    a_number = int(id_match.group(1)) if id_match else None
                else:
                    a_number = None

                if a_number and a_number <= last_id:
                    continue_scraping = False
                    break  # 더 이상의 크롤링이 필요 없으면 반복 중단

                insert_performance = """INSERT INTO PerformancesInfo (Name, Type, concertTime, site, url, siteId, ConcertYm) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
                cursor.execute(insert_performance, (second_cell, 'concert', third_cell, 'yes24', db_url, a_number, '202404'))
                conn.commit()

        cursor.close()

        # 다음 페이지로 넘어가기
        if continue_scraping:
            scrape_and_insert_data(conn, base_url, page_number + 1, last_id)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        session.close()

def main():
    conn = connect_to_database()
    if conn:
        last_id = getLast_id(conn)
        scrape_and_insert_data(conn, last_id)
        conn.close()

if __name__ == "__main__":
    main()
