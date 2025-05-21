# 🎤 concertCrawling

**콘서트 정보 자동 수집 및 Notion 등록 도구**

---

## 📝 프로젝트 소개

이 프로젝트는 **Interpark**와 **Yes24**에서 제공하는 콘서트 정보를 자동으로 크롤링하고,  
이를 **Notion 데이터베이스에 자동으로 등록**하는 Python 기반의 스크립트입니다.

최신 콘서트 정보를 손쉽게 확인하고, 개인 또는 팀 단위의 Notion 관리 도구로 활용할 수 있습니다.

---

## 🔧 기술 스택

- **언어**: Python 3.x
- **크롤링**: `requests`, `BeautifulSoup`
- **Notion 연동**: `notion-client` 또는 `notion-sdk-py`
- **기타**: `datetime`, `json`, `os`

---

## 📁 프로젝트 구조
```
concertCrawling/
├── concertInterpark.py # Interpark 콘서트 정보 크롤러
├── concertYes24.py # Yes24 콘서트 정보 크롤러
├── intoNotionWithYes24.py # 크롤링한 Yes24 데이터를 Notion에 등록
├── crawlingTest.py # 크롤링 테스트용
└── README.md # 이 설명 파일
```

---

## 🚀 실행 방법

### 1. 레포지토리 클론

```bash
git clone https://github.com/nhjin/concertCrawling.git
cd concertCrawling
```

### 의존성 주입 

```bash
pip install requests beautifulsoup4
pip install notion-client  
```

### 🛠️ 향후 개선 사항
* Interpark → Notion 연동
* 중복 등록 방지 로직
* 크론탭 등록으로 자동화
* 로그 기록 및 에러 핸들링 강화