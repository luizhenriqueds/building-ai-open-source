import csv
import io
import logging
import random
import re
from collections import defaultdict

import requests

from pipeline.config import (
    CAIXA_CSV_URL,
    CAIXA_DOWNLOAD_PAGE,
    CAIXA_REQUEST_HEADERS,
    CSV_DELIMITER,
    CSV_HEADER_MARKER,
    CSV_MIN_COLUMNS,
    DATA_DIR,
    DOWNLOADED_FILENAME,
    LAND_TYPES,
    LOCAL_FILE_PATTERN,
    REQUEST_TIMEOUT_SECONDS,
    ROOT_DIR,
    SAMPLE_PATH,
    SAMPLE_SEED,
    SAMPLE_SIZE,
)
from pipeline.schemas import PropertyRecord

logger = logging.getLogger(__name__)

Stratum = tuple[str, str]


def decode(content: bytes) -> str:
    """Decode UTF-8 bytes, falling back to Latin-1.

    Args:
        content: Raw file bytes.
    """
    try:
        return content.decode("utf-8")
    except UnicodeDecodeError:
        return content.decode("latin-1")


def parse_money(value: str) -> float | None:
    """Parse a pt-BR money string such as '136.584,86'.

    Args:
        value: Money text, possibly empty.
    """
    return float(value.replace(".", "").replace(",", ".")) if value else None


def extract_area(label: str, description: str) -> float | None:
    """Extract the area in m² written as 'N de <label>'; zero counts as missing.

    Args:
        label: Text after the number, e.g. 'área privativa'.
        description: CAIXA property description.
    """
    match = re.search(rf"([\d.]+) de {label}", description)
    return (float(match.group(1)) or None) if match else None


def extract_count(label: str, description: str) -> int | None:
    """Extract the integer written as 'N <label>'.

    Args:
        label: Regex for the text after the number, e.g. r'qto\\(s\\)'.
        description: CAIXA property description.
    """
    match = re.search(rf"(\d+) {label}", description)
    return int(match.group(1)) if match else None


def to_property(cells: list[str]) -> PropertyRecord:
    """Convert one CSV row into a property record.

    Args:
        cells: Stripped CSV cells in CAIXA column order.
    """
    (property_id, uf, city, neighborhood, raw_address, sale_value, appraised_value, discount) = (
        cells[:8]
    )
    description, modality, link = cells[9:12]
    built_area = extract_area("área privativa", description) or extract_area(
        "área total", description
    )
    return PropertyRecord(
        **{
            "property_id": property_id,
            "property_type": description.split(",")[0].strip(),
            "uf": uf,
            "city": city,
            "neighborhood": neighborhood,
            "raw_address": raw_address,
            "appraised_value": parse_money(appraised_value),
            "sale_value": parse_money(sale_value),
            "discount": float(discount) if discount else None,
            "modality": modality,
            "link": link,
            "description": description,
            "area_m2": built_area,
            "land_area": extract_area("área do terreno", description),
            "bedrooms": extract_count(r"qto\(s\)", description),
            "parking_spots": extract_count(r"vaga\(s\)", description),
        }
    )


def is_eligible(prop: PropertyRecord) -> bool:
    """Tell whether a property has a link, an address and is not land.

    Args:
        prop: Property record.
    """
    return bool(prop.link and prop.raw_address and prop.property_type not in LAND_TYPES)


def find_header_index(rows: list[list[str]]) -> int:
    """Return the index of the header row, or raise if it is missing.

    Args:
        rows: All parsed CSV rows.
    """
    for index, row in enumerate(rows):
        if CSV_HEADER_MARKER in [cell.strip() for cell in row]:
            return index
    raise ValueError("header row not found (probably the CAIXA block page)")


def parse_listing(text: str) -> list[PropertyRecord]:
    """Parse the CAIXA CSV text into eligible property records.

    Args:
        text: Decoded CSV content.
    """
    rows = list(csv.reader(io.StringIO(text), delimiter=CSV_DELIMITER))
    data_rows = rows[find_header_index(rows) + 1 :]
    properties = (
        to_property([cell.strip() for cell in row])
        for row in data_rows
        if len(row) >= CSV_MIN_COLUMNS
    )
    return [prop for prop in properties if is_eligible(prop)]


def download_properties() -> list[PropertyRecord]:
    """Download a fresh CAIXA list, keep a copy in the data folder and parse it."""
    response = requests.get(
        CAIXA_CSV_URL, headers=CAIXA_REQUEST_HEADERS, timeout=REQUEST_TIMEOUT_SECONDS
    )
    response.raise_for_status()
    properties = parse_listing(decode(response.content))
    DATA_DIR.mkdir(exist_ok=True)
    (DATA_DIR / DOWNLOADED_FILENAME).write_bytes(response.content)
    return properties


def read_local_properties() -> list[PropertyRecord]:
    """Parse the most recently modified CAIXA list in the data folder."""
    local_files = list(DATA_DIR.glob(LOCAL_FILE_PATTERN))
    if not local_files:
        raise FileNotFoundError(
            f"No CSV in {DATA_DIR}: download it manually from {CAIXA_DOWNLOAD_PAGE}"
        )
    latest_file = max(local_files, key=lambda path: path.stat().st_mtime)
    return parse_listing(decode(latest_file.read_bytes()))


def load_properties() -> list[PropertyRecord]:
    """Download the CAIXA list, falling back to the latest local file if blocked."""
    try:
        return download_properties()
    except (requests.RequestException, ValueError) as error:
        logger.warning("Download failed (%s); falling back to the latest local file.", error)
        return read_local_properties()


def group_by_stratum(properties: list[PropertyRecord]) -> dict[Stratum, list[PropertyRecord]]:
    """Group properties by (type, UF), ordered by property id for reproducibility.

    Args:
        properties: Eligible property records.
    """
    strata = defaultdict(list)
    for prop in sorted(properties, key=lambda prop: prop.property_id):
        strata[(prop.property_type, prop.uf)].append(prop)
    return strata


def allocate(stratum_sizes: dict[Stratum, int], sample_size: int) -> dict[Stratum, int]:
    """Split the sample across strata proportionally, by largest remainder.

    Args:
        stratum_sizes: Number of eligible properties per stratum.
        sample_size: Total rows to draw.
    """
    total = sum(stratum_sizes.values())
    quotas = {stratum: sample_size * size / total for stratum, size in stratum_sizes.items()}
    allocation = {stratum: int(quota) for stratum, quota in quotas.items()}
    leftover = sample_size - sum(allocation.values())
    by_largest_remainder = sorted(
        quotas, key=lambda stratum: (allocation[stratum] - quotas[stratum], stratum)
    )
    for stratum in by_largest_remainder[:leftover]:
        allocation[stratum] += 1
    return allocation


def draw_sample(
    strata: dict[Stratum, list[PropertyRecord]], allocation: dict[Stratum, int]
) -> list[PropertyRecord]:
    """Randomly draw the allocated number of properties from each stratum.

    Args:
        strata: Properties grouped by stratum.
        allocation: Rows to draw per stratum.
    """
    random_generator = random.Random(SAMPLE_SEED)
    sample = [
        prop
        for stratum in sorted(strata)
        for prop in random_generator.sample(strata[stratum], allocation[stratum])
    ]
    return sorted(sample, key=lambda prop: prop.property_id)


def log_allocation(
    strata: dict[Stratum, list[PropertyRecord]], allocation: dict[Stratum, int]
) -> None:
    """Log the allocation table for the strata that were sampled.

    Args:
        strata: Properties grouped by stratum.
        allocation: Rows drawn per stratum.
    """
    logger.info("%-16s%-4s%9s%9s", "type", "uf", "eligible", "sampled")
    sampled_strata = [stratum for stratum in allocation if allocation[stratum]]
    for stratum in sorted(sampled_strata, key=lambda stratum: (-allocation[stratum], stratum)):
        property_type, uf = stratum
        logger.info("%-16s%-4s%9d%9d", property_type, uf, len(strata[stratum]), allocation[stratum])
    eligible_total = sum(len(rows) for rows in strata.values())
    logger.info("%-20s%9d%9d", "total", eligible_total, sum(allocation.values()))


def write_sample(sample: list[PropertyRecord]) -> None:
    """Write the sample to the committed CSV, overwriting any previous one.

    Args:
        sample: Property records to save.
    """
    SAMPLE_PATH.parent.mkdir(exist_ok=True)
    with SAMPLE_PATH.open("w", newline="", encoding="utf-8") as sample_file:
        writer = csv.DictWriter(sample_file, fieldnames=list(PropertyRecord.model_fields))
        writer.writeheader()
        writer.writerows(prop.model_dump() for prop in sample)
    logger.info("Saved %s", SAMPLE_PATH.relative_to(ROOT_DIR))


def run() -> None:
    """Draw the stratified sample and save it."""
    strata = group_by_stratum(load_properties())
    allocation = allocate({stratum: len(rows) for stratum, rows in strata.items()}, SAMPLE_SIZE)
    log_allocation(strata, allocation)
    write_sample(draw_sample(strata, allocation))
