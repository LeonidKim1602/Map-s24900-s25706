from typing import Annotated

import requests
from fastapi import FastAPI, Form, Request, Response, Depends
from fastapi.responses import RedirectResponse
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import parse_raw_as

from pjait_map_common.schemas import *
from uuid import UUID
from session import create_session, delete_session, SessionData, cookie

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/login", response_class=HTMLResponse)
def login(request: Request) -> HTMLResponse:
	return templates.TemplateResponse("login.html", {'request': request})
	
@app.post("/login", response_class=HTMLResponse)
async def login(username: Annotated[str, Form()], password: Annotated[str, Form()], request: Request) -> Response:
	request_user = User(number=int(username[1:]), password=password)
	response = requests.post("http://localhost:8001/student", json=request_user.dict())
	
	if response.status_code == 200:
		print("Ok")
		data = SessionData(student_id=request_user.number)
		response = RedirectResponse("/")

		await create_session(response, data)

		return response
		
	elif response.status_code == 404:
		print("No such user")
		return None
	elif response.status_code == 401:
		print("Wrong password")
		return None
	else:
		print("MEGAERROR")
		return None
		
@app.post("/")
@app.get("/")
async def index(session_id: UUID = Depends(cookie)):
	response = Response()
	print(session_id)
	#await delete_session(response, session_id)
	return response
