import csv
import io
import random
import re
from collections import defaultdict
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
SAMPLE_PATH = ROOT / "sample" / "properties.csv"

CSV_URL = "https://venda-imoveis.caixa.gov.br/listaweb/Lista_imoveis_geral.csv"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    ),
    "Referer": "https://venda-imoveis.caixa.gov.br/sistema/download-lista.asp",
}
HEADER_MARKER = "N° do imóvel"
LAND_TYPES = {"Terreno", "Gleba", "Gleba Urbana"}
SAMPLE_SIZE = 100
SEED = 42

COLUMNS = [
    "property_id",
    "property_type",
    "uf",
    "city",
    "neighborhood",
    "raw_address",
    "appraised_value",
    "sale_value",
    "discount",
    "modality",
    "link",
    "description",
    "area_m2",
    "land_area",
    "bedrooms",
    "parking_spots",
]


def decode(content: bytes) -> str:
    try:
        return content.decode("utf-8")
    except UnicodeDecodeError:
        return content.decode("latin-1")


def pt_br_money(value: str) -> float | None:
    return float(value.replace(".", "").replace(",", ".")) if value else None


def number_before(label: str, description: str) -> float | None:
    match = re.search(rf"([\d.]+) de {label}", description)
    return float(match.group(1)) or None if match else None


def count_before(label: str, description: str) -> int | None:
    match = re.search(rf"(\d+) {label}", description)
    return int(match.group(1)) if match else None


def to_property(cells: list[str]) -> dict:
    pid, uf, city, hood, address, price, appraised, discount, _, desc, modality, link = cells[:12]
    built = number_before("área privativa", desc) or number_before("área total", desc)
    return {
        "property_id": pid,
        "property_type": desc.split(",")[0].strip(),
        "uf": uf,
        "city": city,
        "neighborhood": hood,
        "raw_address": address,
        "appraised_value": pt_br_money(appraised),
        "sale_value": pt_br_money(price),
        "discount": float(discount) if discount else None,  # dot-decimal, unlike the money columns
        "modality": modality,
        "link": link,
        "description": desc,
        "area_m2": built,
        "land_area": number_before("área do terreno", desc),
        "bedrooms": count_before(r"qto\(s\)", desc),
        "parking_spots": count_before(r"vaga\(s\)", desc),
    }


def parse_listing(text: str) -> list[dict]:
    rows = list(csv.reader(io.StringIO(text), delimiter=";"))
    start = next((i for i, r in enumerate(rows) if HEADER_MARKER in [c.strip() for c in r]), None)
    if start is None:
        raise ValueError("header row not found (probably the CAIXA block page)")
    properties = (to_property([c.strip() for c in r]) for r in rows[start + 1 :] if len(r) >= 12)
    return [
        p
        for p in properties
        if p["link"] and p["raw_address"] and p["property_type"] not in LAND_TYPES
    ]


def load_properties() -> list[dict]:
    try:
        response = requests.get(CSV_URL, headers=HEADERS, timeout=60)
        response.raise_for_status()
        properties = parse_listing(decode(response.content))
    except (requests.RequestException, ValueError) as error:
        print(f"Download failed ({error}); falling back to the latest local file.")
        local_files = list(DATA_DIR.glob("[Ll]ista_imoveis*.csv"))
        if not local_files:
            raise FileNotFoundError(
                f"Download blocked and no CSV in {DATA_DIR}: download it manually from "
                "https://venda-imoveis.caixa.gov.br/sistema/download-lista.asp"
            ) from error
        return parse_listing(decode(max(local_files, key=lambda f: f.stat().st_mtime).read_bytes()))
    DATA_DIR.mkdir(exist_ok=True)
    (DATA_DIR / "lista_imoveis_geral.csv").write_bytes(response.content)
    return properties


def allocate(sizes: dict, n: int) -> dict:
    """Proportional allocation by largest remainder."""
    total = sum(sizes.values())
    quotas = {key: n * size / total for key, size in sizes.items()}
    allocation = {key: int(quota) for key, quota in quotas.items()}
    leftover = n - sum(allocation.values())
    by_remainder = sorted(quotas, key=lambda key: (allocation[key] - quotas[key], key))
    for key in by_remainder[:leftover]:
        allocation[key] += 1
    return allocation


def stratified_sample(
    properties: list[dict], n: int = SAMPLE_SIZE
) -> tuple[list[dict], dict, dict]:
    strata = defaultdict(list)
    for prop in sorted(properties, key=lambda p: p["property_id"]):
        strata[(prop["property_type"], prop["uf"])].append(prop)
    allocation = allocate({key: len(rows) for key, rows in strata.items()}, n)
    rng = random.Random(SEED)
    sample = [p for key in sorted(strata) for p in rng.sample(strata[key], allocation[key])]
    return sorted(sample, key=lambda p: p["property_id"]), strata, allocation


def run() -> None:
    sample, strata, allocation = stratified_sample(load_properties())
    print(f"{'type':<16}{'uf':<4}{'eligible':>9}{'sampled':>9}")
    for key in sorted(allocation, key=lambda k: (-allocation[k], k)):
        if allocation[key]:
            print(f"{key[0]:<16}{key[1]:<4}{len(strata[key]):>9}{allocation[key]:>9}")
    print(f"{'total':<20}{sum(map(len, strata.values())):>9}{len(sample):>9}")

    SAMPLE_PATH.parent.mkdir(exist_ok=True)
    with SAMPLE_PATH.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(sample)
    print(f"Saved {SAMPLE_PATH.relative_to(ROOT)}")
