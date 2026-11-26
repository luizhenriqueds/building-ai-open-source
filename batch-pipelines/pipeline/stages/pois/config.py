from pipeline.common.config import DATA_DIR

OVERPASS_URLS = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
]
OVERPASS_USER_AGENT = "semantic-lens-lite/0.1 (open-source real-estate demo)"
OVERPASS_TIMEOUT_SECONDS = 330
OVERPASS_ROUNDS = 3
OVERPASS_RETRY_PAUSE_SECONDS = 30
POIS_CACHE_DIR = DATA_DIR / "cache"

POI_RADIUS_M = 5000
POIS_PER_CATEGORY = 10

AMENITIES = [
    "hospital",
    "school",
    "pharmacy",
    "bank",
    "restaurant",
    "cafe",
    "university",
    "college",
    "police",
    "bus_station",
]
SHOPS = ["supermarket", "mall"]
SELECTORS = [
    f'["amenity"~"^({"|".join(AMENITIES)})$"]',
    f'["shop"~"^({"|".join(SHOPS)})$"]',
    '["leisure"="park"]',
]
CATEGORY_ALIASES = {"college": "university", "mall": "shopping_center"}
