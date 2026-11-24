import os
import re
from pathlib import Path

DATABASE_URL = os.environ.get(
    "DATABASE_URL", "postgresql+psycopg://postgres:postgres@127.0.0.1:55322/postgres"
)

ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "data"
SAMPLE_PATH = ROOT_DIR / "sample" / "properties.csv"
IMAGES_DIR = DATA_DIR / "images"

CAIXA_CSV_URL = "https://venda-imoveis.caixa.gov.br/listaweb/Lista_imoveis_geral.csv"
CAIXA_REQUEST_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    ),
    "Referer": "https://venda-imoveis.caixa.gov.br/sistema/download-lista.asp",
}
CAIXA_DOWNLOAD_PAGE = "https://venda-imoveis.caixa.gov.br/sistema/download-lista.asp"
DOWNLOADED_FILENAME = "lista_imoveis_geral.csv"
LOCAL_FILE_PATTERN = "[Ll]ista_imoveis*.csv"
REQUEST_TIMEOUT_SECONDS = 60
CSV_DELIMITER = ";"
CSV_HEADER_MARKER = "N° do imóvel"
CSV_MIN_COLUMNS = 12

LAND_TYPES = {"Terreno", "Gleba", "Gleba Urbana"}
SAMPLE_SIZE = 100
SAMPLE_SEED = 42

CAIXA_BASE_URL = "https://venda-imoveis.caixa.gov.br"
CRAWL_MAX_SESSIONS = 2
CRAWL_DELAY_RANGE_SECONDS = (1.0, 2.5)
CRAWL_MAX_RETRIES = 3
CRAWL_PAGE_TIMEOUT_MS = 60000
CRAWL_WAIT_TIMEOUT_MS = 35000
CRAWL_RATE_LIMIT_CODES = [400, 403, 429, 503]
# The detail page is built by JS: wait for its marker, then for the auction box that loads via XHR.
CRAWL_WAIT_FOR = (
    "js:() => { const body = document.body; if (!body) return false;"
    " if (!body.innerText.includes('Número do imóvel')) return false;"
    " const box = document.getElementById('divContador');"
    " if (!box || box.innerHTML.trim()) return true;"
    " window.__boxSince = window.__boxSince || Date.now();"
    " return Date.now() - window.__boxSince > 20000; }"
)

# Radware answers 200 with its interstitial, so only the body tells it apart from a real page.
BLOCKED_PATTERN = re.compile(
    r"Radware Bot Manager|SSJSConnector|perfdrive|comportamento malicioso", re.I
)
# The rendered markdown bolds values ("Área total = **98,07m2**"), hence the optional markup.
BEDROOMS_PATTERN = re.compile(r"Quartos:\s*\**\s*(\d+)")
TOTAL_AREA_PATTERN = re.compile(r"Área total\s*=\s*\**\s*([\d.,]+)\s*m", re.I)
PRIVATE_AREA_PATTERN = re.compile(r"Área privativa\s*=\s*\**\s*([\d.,]+)\s*m", re.I)
LAND_AREA_PATTERN = re.compile(r"Área do terreno\s*=\s*\**\s*([\d.,]+)\s*m", re.I)
OCCUPANCY_PATTERN = re.compile(r"Situação:\s*\**\s*([A-Za-zÀ-ú]+)")
ADDRESS_PATTERN = re.compile(r"\*\*Endere[çc]o:\*\*[ \t]*\n?[ \t]*([^\n]+)", re.I)
AUCTION_DATE_PATTERN = re.compile(
    r"Data\s+d[oa]\s+[^-<\n]{3,40}?\s*-\s*(?P<day>\d{2})/(?P<month>\d{2})/(?P<year>\d{4})", re.I
)
PREVIEW_PHOTO_PATTERN = re.compile(r'id="preview"[^>]*\bsrc="(/fotos/F\d+\.jpg)"', re.I)
ANY_PHOTO_PATTERN = re.compile(r'"(/fotos/F\d+\.jpg)"', re.I)
