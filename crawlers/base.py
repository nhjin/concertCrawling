from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path

DATA_DIR = Path("data")
INITIAL_LOAD_COUNT = 10


class BaseCrawler(ABC):
    site: str

    @property
    def data_path(self) -> Path:
        return DATA_DIR / f"{self.site}.json"

    def load_store(self) -> dict:
        if self.data_path.exists():
            with open(self.data_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"site": self.site, "flag_id": None, "last_crawled_at": None, "items": []}

    def save_store(self, store: dict) -> None:
        DATA_DIR.mkdir(exist_ok=True)
        with open(self.data_path, "w", encoding="utf-8") as f:
            json.dump(store, f, ensure_ascii=False, indent=2)

    async def run(self) -> None:
        store = self.load_store()
        is_initial = store["flag_id"] is None

        try:
            if is_initial:
                new_items = await self.fetch_initial()
            else:
                new_items = await self.fetch_incremental(store["flag_id"])
        except Exception as e:
            print(f"[{self.site}] Crawl failed: {e}")
            return

        if not new_items:
            print(f"[{self.site}] No new items.")
            return

        store["items"] = new_items + store["items"]
        store["flag_id"] = new_items[0]["id"]
        store["last_crawled_at"] = datetime.now().isoformat()
        self.save_store(store)
        print(f"[{self.site}] {len(new_items)} new item(s) saved.")

    @abstractmethod
    async def fetch_initial(self) -> list[dict]:
        ...

    @abstractmethod
    async def fetch_incremental(self, flag_id: str) -> list[dict]:
        ...
