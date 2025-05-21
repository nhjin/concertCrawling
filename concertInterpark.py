import requests
from bs4 import BeautifulSoup
import mysql.connector
from urllib.parse import urlparse, parse_qs
from datetime import datetime

def connect_to_database():
    try:
        conn = mysql.connector.connect(
            host='',
            user='',
            password='',
            database='',
            port=3306
        )
        if conn.is_connected():
            print("Successfully connected to the database")
            return conn
        else:
            print("Connection failed")
            return None
    except mysql.connector.Error as e:
        print(f"Database connection failed: {e}")
        return None

def getLast_id(conn):
    # SQL 쿼리를 정의합니다.
    query = """
    SELECT MAX(siteId) FROM PerformancesInfo
    WHERE site = 'interpark'
    """

    # 커서를 생성하고 쿼리를 실행합니다.
    cursor = conn.cursor()
    cursor.execute(query)
    max_id = cursor.fetchone()[0]  # 결과를 가져옵니다.
    cursor.close()  # 커서와 연결을 정리합니다.
    return max_id

def scrape_data(conn, last_id, page_number=1):
    base_url = 'https://ticket.interpark.com/webzine/paper/'
    iframe_url = f'{base_url}TPNoticeList_iFrame.asp?bbsno=34&stext=&KindOfGoods=TICKET&genre=&sort=WriteDate&pageno={page_number}'
    response = requests.get(iframe_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    rows = soup.find_all('tr')

    cursor = conn.cursor()
    continue_scraping = True

    for row in rows:
        cells = row.find_all('td')
        if len(cells) >= 4:
            type_text = cells[0].get_text(strip=True)
            subject = cells[1].find('a')
            if subject:
                subject_text = subject.get_text(strip=True)
                subject_url = base_url + subject['href']
                parsed_url = urlparse(subject_url)
                query_params = parse_qs(parsed_url.query)
                no_value = int(query_params.get('no', ['0'])[0])

                if no_value <= last_id:
                    continue_scraping = False
                    break  # Stop scraping if the current item's ID is not greater than the last scraped ID

                date_text = cells[2].get_text(strip=True)
                insert_performance = """INSERT INTO PerformancesInfo (Type, Name, concertTime, site, url, siteId, ConcertYm) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
                cursor.execute(insert_performance, (type_text, subject_text, date_text, "interpark", subject_url, no_value, datetime.now().strftime("%Y%m")))
                conn.commit()

    cursor.close()

    # Continue scraping the next page if applicable
    if continue_scraping:
        scrape_data(conn, last_id, page_number + 1)

def main():
    conn = connect_to_database()
    if conn:
        last_id = getLast_id(conn)
        scrape_data(conn, last_id)
        conn.close()

if __name__ == "__main__":
    main()
