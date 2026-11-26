import os
from pathlib import Path

DATABASE_URL = os.environ.get(
    "DATABASE_URL", "postgresql+psycopg://postgres:postgres@127.0.0.1:55322/postgres"
)

ROOT_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT_DIR / "data"
SAMPLE_PATH = ROOT_DIR / "sample" / "properties.csv"

CAIXA_REQUEST_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    ),
    "Referer": "https://venda-imoveis.caixa.gov.br/sistema/download-lista.asp",
}
REQUEST_TIMEOUT_SECONDS = 60
OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
EMBED_MODEL = os.environ.get("EMBED_MODEL", "qwen3-embedding:0.6b")
VISUAL_MODEL = os.environ.get("VISUAL_MODEL", "qwen3.5:9b")

VISUAL_TEMPERATURE = 0
VISUAL_SEED = 42
VISUAL_TIMEOUT_SECONDS = 600
VISUAL_NUM_CTX = 8192
