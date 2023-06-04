from typing import Annotated

from fastapi import Cookie, Depends, FastAPI, Response
from fastapi.responses import RedirectResponse

from dependencies import DatabaseManager, authenticate_user
from routers import user_router, schedule_router


app = FastAPI(dependencies=[Depends(DatabaseManager.get_db)])

app.include_router(user_router)
app.include_router(schedule_router)


@app.get("/")
async def root(auth_cookie: Annotated[str | None, Cookie()] = None) -> Response:
    if auth_cookie is None or authenticate_user(auth_cookie) is None:
        return RedirectResponse("/user/login")
    return RedirectResponse("/schedule")


@app.on_event("startup")
async def startup() -> None:
    DB_URL = "sqlite:///test.db"
    DatabaseManager.connect(DB_URL)


@app.on_event("shutdown")
async def shutdown() -> None:
    DatabaseManager.disconnect()
