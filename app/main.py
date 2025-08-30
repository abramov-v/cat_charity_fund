from fastapi import FastAPI

from app.core.config import settings

app = FastAPI(title=settings.app_name)

app.include_router(main_router)
