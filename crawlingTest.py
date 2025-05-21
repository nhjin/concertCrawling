from requests_html import HTMLSession
import re

#yes24
# session = HTMLSession()
# url = 'http://ticket.yes24.com/New/Notice/NoticeMain.aspx'
#
# r = session.get(url)
# r.html.render()  # JavaScript 렌더링을 위해 호출
#
# # 이제 페이지의 HTML은 JavaScript가 렌더링된 후의 상태를 반영합니다.
# # ID가 'BoardList'인 요소 내의 모든 'tr' 태그 찾기
# rows = r.html.find('#BoardList tr')
#
# for row in rows[1:]:  # 첫 번째 행을 제외하고 반복
#     # 각 행의 'td' 태그 찾기
#     cells = row.find('td')
#
#     if len(cells) >= 3:  # 'td' 태그가 적어도 3개 있는지 확인
#         second_cell = cells[1].text  # 두 번째 'td' 태그의 텍스트
#         third_cell = cells[2].text   # 세 번째 'td' 태그의 텍스트
#
#         # 'a' 태그의 'href' 속성에서 숫자 추출
#         a_tag = cells[1].find('a', first=True)
#         if a_tag:
#             href = a_tag.attrs.get('href', '')
#             id_match = re.search(r'#id=(\d+)', href)
#             if id_match:
#                 a_number = id_match.group(1)  # 'a' 태그 내의 숫자
#             else:
#                 a_number = 'Not found'
#         else:
#             a_number = 'Not found'
#
#         print(second_cell, third_cell, a_number)
#
# session.close()

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
