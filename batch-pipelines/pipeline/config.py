import os
from pathlib import Path

DATABASE_URL = os.environ.get(
    "DATABASE_URL", "postgresql+psycopg://postgres:postgres@127.0.0.1:55322/postgres"
)

ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "data"
SAMPLE_PATH = ROOT_DIR / "sample" / "properties.csv"

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

OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
EMBED_MODEL = os.environ.get("EMBED_MODEL", "qwen3-embedding:0.6b")
