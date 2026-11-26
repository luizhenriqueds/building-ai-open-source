import re

from pipeline.common.config import DATA_DIR

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
NOMINATIM_PARAMS = {"format": "jsonv2", "countrycodes": "br", "limit": 1}
NOMINATIM_USER_AGENT = "semantic-lens-lite/0.1 (open-source real-estate demo)"
NOMINATIM_INTERVAL_SECONDS = 1.0
GEOCODE_CACHE_PATH = DATA_DIR / "cache" / "geocode.json"

MAX_DISTANCE_FROM_CITY_KM = 25
EARTH_RADIUS_KM = 6371.0
PRECISION_CONFIDENCE = {"street": 0.9, "neighborhood": 0.5, "city": 0.3}

# Matches "RUA XI,N. SN LT 02" and "RUA A, N. 673, Apto 102"; the number group skips "SN"/"S/N".
STREET_NUMBER_PATTERN = re.compile(r"^(?P<street>[^,]+),\s*N\.\s*(?P<number>\d+)?", re.I)
# Streets such as "QUADRA 33" or "LOTE 4" are plots, not searchable street names.
PLOT_STREET_PATTERN = re.compile(r"^(quadra|qd|lote|lt|casa|cs)\b", re.I)
