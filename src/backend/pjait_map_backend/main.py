import os
from typing import Annotated

from fastapi import Depends, FastAPI

from dependencies import DatabaseManager
from routers import user_router, schedule_router


app = FastAPI(dependencies=[Depends(DatabaseManager.get_db)])

app.include_router(user_router)
app.include_router(schedule_router)


@app.on_event("startup")
async def startup() -> None:
    default_url = "sqlite:///test.db"
    db_url = os.getenv("DB_URL", default_url)

    DatabaseManager.connect(db_url)


@app.on_event("shutdown")
async def shutdown() -> None:
    DatabaseManager.disconnect()