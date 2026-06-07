from __future__ import annotations

import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime

from .base import BaseCrawler, INITIAL_LOAD_COUNT

API_URL = "https://ticket.yes24.com/New/Notice/Ajax/axList.aspx"
DETAIL_BASE = "https://ticket.yes24.com/New/Notice/NoticeMain.aspx"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Referer": "https://ticket.yes24.com/New/Notice/NoticeMain.aspx",
}


def _fetch_page(page_no: int) -> list[dict]:
    params = {
        "Page": page_no,
        "PageSize": 20,
        "SearchType": "All",
        "Genre": "",
        "Order": "",
    }
    resp = requests.get(API_URL, params=params, headers=HEADERS, timeout=10)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    rows = soup.select("table tbody tr")
    now = datetime.now()
    items = []

    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 3:
            continue

        a_tag = cols[1].find("a")
        if not a_tag:
            continue

        href = a_tag.get("href", "")
        m = re.search(r'id=(\d+)', href)
        if not m:
            continue

        notice_id = m.group(1)

        items.append({
            "id": notice_id,
            "title": a_tag.get_text(strip=True),
            "place": "",
            "open_time": cols[2].get_text(strip=True),
            "open_type": cols[0].get_text(strip=True),
            "badges": [],
            "thumbnail": "",
            "source_url": f"{DETAIL_BASE}?id={notice_id}",
            "site": "yes24",
            "crawled_at": now.isoformat(),
        })

    return items


def _collect(flag_id: str | None, max_items: int | None) -> list[dict]:
    collected: list[dict] = []
    page_no = 1

    while True:
        rows = _fetch_page(page_no)
        if not rows:
            break

        for item in rows:
            if flag_id and item["id"] == flag_id:
                return collected
            collected.append(item)
            if max_items and len(collected) >= max_items:
                return collected

        page_no += 1

    return collected


class Yes24Crawler(BaseCrawler):
    site = "yes24"

    async def fetch_initial(self) -> list[dict]:
        return _collect(flag_id=None, max_items=INITIAL_LOAD_COUNT)

    async def fetch_incremental(self, flag_id: str) -> list[dict]:
        return _collect(flag_id=flag_id, max_items=None)
