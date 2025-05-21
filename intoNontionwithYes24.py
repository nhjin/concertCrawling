import requests

NOTION_TOKEN = ''  # 여기에 앞서 생성한 Secret 토큰을 입력하세요.
PAGE_ID = ''  # 접근하려는 Notion 페이지의 ID를 입력하세요.
DATABASE_ID = ""  # Database ID for your database



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