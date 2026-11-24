import asyncio
import logging
from datetime import date

import requests
from crawl4ai import (
    AsyncWebCrawler,
    BrowserConfig,
    CacheMode,
    CrawlerRunConfig,
    MemoryAdaptiveDispatcher,
    RateLimiter,
)
from sqlalchemy import select

from pipeline.config import (
    CAIXA_REQUEST_HEADERS,
    REQUEST_TIMEOUT_SECONDS,
)
from pipeline.crawl_config import (
    ADDRESS_PATTERN,
    ANY_PHOTO_PATTERN,
    AUCTION_DATE_PATTERN,
    BEDROOMS_PATTERN,
    BLOCKED_PATTERN,
    CAIXA_BASE_URL,
    CRAWL_DELAY_RANGE_SECONDS,
    CRAWL_MAX_RETRIES,
    CRAWL_MAX_SESSIONS,
    CRAWL_PAGE_TIMEOUT_MS,
    CRAWL_RATE_LIMIT_CODES,
    CRAWL_WAIT_FOR,
    CRAWL_WAIT_TIMEOUT_MS,
    IMAGES_DIR,
    LAND_AREA_PATTERN,
    OCCUPANCY_PATTERN,
    PREVIEW_PHOTO_PATTERN,
    PRIVATE_AREA_PATTERN,
    TOTAL_AREA_PATTERN,
)
from pipeline.db import get_session
from pipeline.models import Property
from pipeline.schemas import PageDetails

logger = logging.getLogger(__name__)

Page = tuple[str, str]


class BlockedError(RuntimeError):
    """CAIXA answered with its anti-bot page instead of the property page."""


def is_blocked(html: str) -> bool:
    """Tell whether the response is the anti-bot page.

    Args:
        html: Rendered page HTML.
    """
    return bool(BLOCKED_PATTERN.search(html))


def find_text(pattern, text: str) -> str | None:
    """Return the first capture group of a pattern, stripped, or None.

    Args:
        pattern: Compiled regex with one capture group.
        text: Text to search.
    """
    match = pattern.search(text)
    return match.group(1).strip() if match else None


def find_area(pattern, text: str) -> float | None:
    """Return a pt-BR area such as '1.627,18' as a float; zero counts as missing.

    Args:
        pattern: Compiled regex capturing the number.
        text: Text to search.
    """
    value = find_text(pattern, text)
    return float(value.replace(".", "").replace(",", ".")) or None if value else None


def parse_auction_date(markdown: str) -> date | None:
    """Return the first dated auction line ('Data do 1º Leilão - 03/08/2026'), or None.

    Args:
        markdown: Rendered page markdown.
    """
    match = AUCTION_DATE_PATTERN.search(markdown)
    if not match:
        return None
    try:
        return date(int(match["year"]), int(match["month"]), int(match["day"]))
    except ValueError:
        return None


def parse_image_url(html: str) -> str | None:
    """Return the absolute URL of the main photo, or None.

    Args:
        html: Rendered page HTML.
    """
    path = find_text(PREVIEW_PHOTO_PATTERN, html) or find_text(ANY_PHOTO_PATTERN, html)
    return CAIXA_BASE_URL + path if path else None


def parse_page(html: str, markdown: str) -> PageDetails:
    """Extract the detail fields from a rendered property page.

    Args:
        html: Rendered page HTML (photo).
        markdown: Rendered page markdown (everything else).
    """
    bedrooms = find_text(BEDROOMS_PATTERN, markdown)
    return PageDetails(
        bedrooms=int(bedrooms) if bedrooms else None,
        area_m2=find_area(PRIVATE_AREA_PATTERN, markdown)
        or find_area(TOTAL_AREA_PATTERN, markdown),
        land_area=find_area(LAND_AREA_PATTERN, markdown),
        occupancy_status=find_text(OCCUPANCY_PATTERN, markdown),
        raw_address=find_text(ADDRESS_PATTERN, markdown),
        auction_date=parse_auction_date(markdown),
        image_url=parse_image_url(html),
    )


async def render_pages(links: list[str]) -> dict[str, Page]:
    """Render property pages in one headless browser.

    Args:
        links: CAIXA detail page URLs.
    """
    run_config = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        wait_for=CRAWL_WAIT_FOR,
        wait_for_timeout=CRAWL_WAIT_TIMEOUT_MS,
        page_timeout=CRAWL_PAGE_TIMEOUT_MS,
    )
    dispatcher = MemoryAdaptiveDispatcher(
        max_session_permit=CRAWL_MAX_SESSIONS,
        rate_limiter=RateLimiter(
            base_delay=CRAWL_DELAY_RANGE_SECONDS,
            max_retries=CRAWL_MAX_RETRIES,
            rate_limit_codes=CRAWL_RATE_LIMIT_CODES,
        ),
    )
    browser_config = BrowserConfig(headless=True, text_mode=True, verbose=False)
    async with AsyncWebCrawler(config=browser_config) as crawler:
        results = await crawler.arun_many(urls=links, config=run_config, dispatcher=dispatcher)
    return {
        result.url: (result.html, getattr(result.markdown, "raw_markdown", result.markdown) or "")
        for result in results
        if result.success and result.html
    }


def render_with_retries(links: list[str]) -> dict[str, Page]:
    """Render pages, retrying the ones that failed to render.

    Args:
        links: CAIXA detail page URLs.
    """
    pages: dict[str, Page] = {}
    for _ in range(CRAWL_MAX_RETRIES):
        pending = [link for link in links if link not in pages]
        if not pending:
            break
        pages.update(asyncio.run(render_pages(pending)))
    return pages


def download_image(image_url: str, property_id: str) -> str | None:
    """Download the main photo to the images folder and return its file name.

    Args:
        image_url: Absolute photo URL.
        property_id: CAIXA property id, used as the file name.
    """
    try:
        response = requests.get(
            image_url, headers=CAIXA_REQUEST_HEADERS, timeout=REQUEST_TIMEOUT_SECONDS
        )
        response.raise_for_status()
    except requests.RequestException as error:
        logger.warning("%s: photo download failed (%s)", property_id, error)
        return None
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    file_name = f"{property_id}.jpg"
    (IMAGES_DIR / file_name).write_bytes(response.content)
    return file_name


def apply_page(prop: Property, html: str, markdown: str) -> None:
    """Copy the page details and the downloaded photo onto a property.

    Args:
        prop: Property row to update.
        html: Rendered page HTML.
        markdown: Rendered page markdown.
    """
    details = parse_page(html, markdown)
    for field, value in details.model_dump(exclude={"image_url"}, exclude_none=True).items():
        setattr(prop, field, value)
    if details.image_url:
        prop.image_file = download_image(details.image_url, prop.property_id)


def run(limit: int | None = None) -> None:
    """Crawl the detail page and photo of properties that have no photo yet.

    Args:
        limit: Maximum number of properties to crawl; None crawls all of them.
    """
    with get_session() as session:
        query = select(Property).where(Property.image_file.is_(None)).order_by(Property.property_id)
        properties = {prop.link: prop for prop in session.scalars(query.limit(limit))}
        pages = render_with_retries(list(properties))
        blocked = 0
        for link, (html, markdown) in pages.items():
            if is_blocked(html):
                blocked += 1
            else:
                apply_page(properties[link], html, markdown)
        session.commit()
    logger.info("Crawled %d/%d pages", len(pages) - blocked, len(properties))
    if blocked:
        raise BlockedError(
            f"CAIXA's anti-bot blocked {blocked} page(s). Wait ~30 minutes or change network, "
            "then run `pipeline crawl` again; finished properties are kept."
        )
