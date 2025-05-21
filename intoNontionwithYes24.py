import requests

NOTION_TOKEN = 'secret_MiO4EZ1o6YReFCXK2hI3nYQkIm481UKTnZ2VIOVqnYn'  # 여기에 앞서 생성한 Secret 토큰을 입력하세요.
PAGE_ID = '83b812d3eda7468aa3cf6104f75056f0'  # 접근하려는 Notion 페이지의 ID를 입력하세요.
DATABASE_ID = "c58a13b20416439e944d3095d50b3194"  # Database ID for your database

# headers = {
#     "Authorization": f"Bearer {NOTION_TOKEN}",
#     "Content-Type": "application/json",
#     "Notion-Version": "2022-06-28"  # API 버전은 Notion의 최신 버전으로 설정하세요.
# }
#
# data = {
#     "parent": {"page_id": PAGE_ID},
#     "properties": {
#         "title": {
#             "title": [
#                 {
#                     "text": {
#                         "content": "제목입니다"
#                     }
#                 }
#             ]
#         }
#     },
#     "children": [
#         {
#             "object": "block",
#             "type": "paragraph",
#             "paragraph": {
#                 "rich_text": [  # 'text' 대신 'rich_text'를 사용
#                     {
#                         "type": "text",
#                         "text": {
#                             "content": "여기에 내용을 입력하세요.",
#                             "link": None
#                         }
#                     }
#                 ]
#             }
#         }
#     ]
# }
#
#
# response = requests.post('https://api.notion.com/v1/pages', headers=headers, json=data)
# print(response.text)  # 응답을 출력하여 결과를 확인할 수 있습니다.


headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

data = {
    "parent": {"database_id": DATABASE_ID},
    "properties": {
        "이름": {
            "title": [
                {
                    "text": {
                        "content": "새 이벤트222"
                    }
                }
            ]
        },
        "날짜": {
            "date": {
                "start": "2024-05-01",
                "end": "2024-05-02"
            }
        },
        "태그": {
            "multi_select": [
                {
                    "name": "중요"
                }
            ]
        }
    }
}


response = requests.post('https://api.notion.com/v1/pages', headers=headers, json=data)
if response.status_code == 200:
    print("성공적으로 페이지가 생성되었습니다.")
else:
    print("페이지 생성에 실패했습니다.")
    print(f"상태 코드: {response.status_code}")
    print(f"오류 메시지: {response.text}")