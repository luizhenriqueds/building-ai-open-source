from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from api.routes import router
from pipeline.config import API_CORS_ORIGINS
from pipeline.crawl_config import IMAGES_DIR

app = FastAPI(title="Houses Ranking API")
app.add_middleware(CORSMiddleware, allow_origins=API_CORS_ORIGINS, allow_methods=["GET"])
app.include_router(router)
app.mount("/images", StaticFiles(directory=IMAGES_DIR, check_dir=False), name="images")
