import asyncio

from crawlers.interpark import InterparkCrawler
from crawlers.yes24 import Yes24Crawler
from crawlers.ticketlink import TicketLinkCrawler


async def main() -> None:
    crawlers = [InterparkCrawler(), Yes24Crawler(), TicketLinkCrawler()]
    results = await asyncio.gather(*[c.run() for c in crawlers], return_exceptions=True)

    for crawler, result in zip(crawlers, results):
        if isinstance(result, Exception):
            print(f"[{crawler.site}] Unhandled error: {result}")


if __name__ == "__main__":
    asyncio.run(main())
