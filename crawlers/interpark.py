from __future__ import annotations

import re
from datetime import datetime, timedelta
from playwright.async_api import async_playwright, Page

from .base import BaseCrawler, INITIAL_LOAD_COUNT

URL = "https://tickets.interpark.com/contents/notice"

# CSS 모듈 해시는 빌드마다 바뀔 수 있으므로 [class*=] 선택자 사용
ITEM_SEL = '[class*="NoticeItem_ticketItem"]'


def _extract_goods_id(src: str) -> str:
    # /Play/image/large/26/26008330_p.gif → "26008330"
    m = re.search(r'/(\d{6,})_p\.', src)
    if m:
        return m.group(1)
    # /TicketImage/notice_poster/20/20260514050808.jpg → "20260514050808"
    m = re.search(r'/(\d{10,})\.\w+$', src)
    if m:
        return m.group(1)
    return str(abs(hash(src)))


def _parse_open_time(raw: str, now: datetime) -> str:
    raw = raw.strip().split("\n")[0].strip()
    if "오늘" in raw:
        t = raw.replace("오늘", "").strip()
        return f"{now.strftime('%Y-%m-%d')} {t}"
    if "내일" in raw:
        t = raw.replace("내일", "").strip()
        return f"{(now + timedelta(days=1)).strftime('%Y-%m-%d')} {t}"
    return raw


async def _parse_element(el, now: datetime) -> dict | None:
    title = (await el.get_attribute("gtm-label") or "").strip()

    img = await el.query_selector("img")
    thumbnail = (await img.get_attribute("src") or "") if img else ""
    goods_id = _extract_goods_id(thumbnail)

    play_date_el = await el.query_selector('[class*="NoticeItem_playDate"]')
    raw_time = (await play_date_el.inner_text() if play_date_el else "").strip()
    open_time = _parse_open_time(raw_time, now)

    place_el = await el.query_selector('[class*="NoticeItem_placeName"]')
    place = (await place_el.inner_text() if place_el else "").strip()

    type_el = await el.query_selector('[class*="NoticeItem_openType"]')
    open_type = (await type_el.inner_text() if type_el else "").strip()

    badge_els = await el.query_selector_all('[class*="NoticeSingleBadge_seatBadge"]')
    badges = [(await b.inner_text()).strip() for b in badge_els]

    if not goods_id or not title:
        return None

    return {
        "id": goods_id,
        "title": title,
        "place": place,
        "open_time": open_time,
        "open_type": open_type,
        "badges": badges,
        "thumbnail": thumbnail,
        "source_url": f"https://tickets.interpark.com/goods/{goods_id}",
        "site": "interpark",
        "crawled_at": now.isoformat(),
    }


async def _collect(page: Page, flag_id: str | None, max_items: int | None) -> list[dict]:
    now = datetime.now()
    seen_ids: set[str] = set()
    collected: list[dict] = []

    while True:
        elements = await page.query_selector_all(ITEM_SEL)
        new_this_round = False

        for el in elements:
            img = await el.query_selector("img")
            thumbnail = (await img.get_attribute("src") or "") if img else ""
            goods_id = _extract_goods_id(thumbnail)

            if goods_id in seen_ids:
                continue
            seen_ids.add(goods_id)
            new_this_round = True

            if flag_id and goods_id == flag_id:
                return collected

            item = await _parse_element(el, now)
            if item:
                collected.append(item)

            if max_items and len(collected) >= max_items:
                return collected

        if not new_this_round:
            break

        prev_height = await page.evaluate("document.body.scrollHeight")
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await page.wait_for_timeout(2000)
        new_height = await page.evaluate("document.body.scrollHeight")

        if new_height == prev_height:
            break

    return collected


class InterparkCrawler(BaseCrawler):
    site = "interpark"

    async def _crawl(self, flag_id: str | None = None, max_items: int | None = None) -> list[dict]:
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            await page.goto(URL, wait_until="networkidle", timeout=30000)
            await page.wait_for_selector(ITEM_SEL, timeout=15000)
            items = await _collect(page, flag_id=flag_id, max_items=max_items)
            await browser.close()
        return items

    async def fetch_initial(self) -> list[dict]:
        return await self._crawl(max_items=INITIAL_LOAD_COUNT)

    async def fetch_incremental(self, flag_id: str) -> list[dict]:
        return await self._crawl(flag_id=flag_id, max_items=20)
