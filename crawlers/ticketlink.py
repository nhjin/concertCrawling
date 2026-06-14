from __future__ import annotations

import requests
from datetime import datetime

from .base import BaseCrawler, INITIAL_LOAD_COUNT

API_URL = "https://www.ticketlink.co.kr/help/getNoticeList"
DETAIL_BASE = "https://www.ticketlink.co.kr/help/notice/"
HEADERS = {"Referer": "https://www.ticketlink.co.kr/help/notice"}


def _fetch_page(page_no: int) -> list[dict]:
    params = {
        "page": page_no,
        "noticeCategoryCode": "TICKET_OPEN",
        "title": "",
        "sortCode": "",
    }
    resp = requests.get(API_URL, params=params, headers=HEADERS, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    return data.get("result", {}).get("result", [])


def _parse_open_time(raw: dict) -> str:
    ts_ms = raw.get("ticketOpenDatetime")
    if ts_ms:
        return datetime.fromtimestamp(ts_ms / 1000).strftime("%Y-%m-%d %H:%M")
    return ""


def _to_item(raw: dict, now: datetime) -> dict:
    notice_id = str(raw["noticeId"])
    return {
        "id": notice_id,
        "title": raw.get("title", ""),
        "place": raw.get("placeName", ""),
        "open_time": _parse_open_time(raw),
        "open_type": raw.get("noticeCategoryName", "티켓오픈"),
        "badges": [],
        "thumbnail": "",
        "source_url": f"{DETAIL_BASE}{notice_id}",
        "site": "ticketlink",
        "crawled_at": now.isoformat(),
    }


def _collect(flag_id: str | None, max_items: int | None) -> list[dict]:
    now = datetime.now()
    collected: list[dict] = []
    page_no = 1

    while True:
        rows = _fetch_page(page_no)
        if not rows:
            break

        for raw in rows:
            if flag_id and str(raw["noticeId"]) == flag_id:
                return collected
            collected.append(_to_item(raw, now))
            if max_items and len(collected) >= max_items:
                return collected

        page_no += 1

    return collected


class TicketLinkCrawler(BaseCrawler):
    site = "ticketlink"

    async def fetch_initial(self) -> list[dict]:
        return _collect(flag_id=None, max_items=INITIAL_LOAD_COUNT)

    async def fetch_incremental(self, flag_id: str) -> list[dict]:
        return _collect(flag_id=flag_id, max_items=20)
