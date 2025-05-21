from requests_html import HTMLSession
import re


#인터파크
import requests
from bs4 import BeautifulSoup

# 메인 페이지 URL
main_url = 'https://ticket.interpark.com/webzine/paper/TPNoticeList.asp?tid1=in_scroll&tid2=ticketopen&tid3=board_main&tid4=board_main'

# 메인 페이지에서 HTML 가져오기
response = requests.get(main_url)
soup = BeautifulSoup(response.content, 'html.parser')

# 아이프레임의 src 속성 찾기
iframe = soup.find('iframe')
iframe_src = iframe['src'] if iframe else None

front_url = 'https://ticket.interpark.com/webzine/paper/'

real_url = front_url + iframe_src

# 아이프레임의 콘텐츠 가져오기
if real_url:
    iframe_response = requests.get(real_url)
    iframe_soup = BeautifulSoup(iframe_response.content, 'html.parser')
    # iframe_soup에서 필요한 데이터 추출
    # 모든 'tr' 태그 찾기
    rows = iframe_soup.find_all('tr')

    # 각 'tr' 태그에 대해 반복
    for row in rows:
        # 현재 행의 모든 'td' 태그 찾기
        cells = row.find_all('td')

        # 각 'td' 태그의 텍스트 추출 및 출력
        for cell in cells:
            print(cell.get_text(strip=True))



#같은 형식으로 이슈데이터도 가져오기
