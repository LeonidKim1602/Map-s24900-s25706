from typing import Annotated

import requests
import datetime
from fastapi import FastAPI, Form, Request, Response, Depends
from fastapi.responses import RedirectResponse
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import parse_raw_as

from pjait_map_common.schemas import *
from uuid import UUID
from session import create_session, delete_session, SessionData, cookie, verifier

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

		
@app.post("/", dependencies=[Depends(cookie)])
@app.get("/", dependencies=[Depends(cookie)])
async def index(request: Request, session_data: SessionData = Depends(verifier)):
	response = requests.get(f"http://localhost:8001/schedule/student/{session_data.student_id}")
	response_schedules = parse_raw_as(list[Schedule], response.text)
	weekday = datetime.datetime.today().weekday()
	today = [s for s in response_schedules if s.weekday == weekday]
	locations = []
	
	for schedule in today:
		resp = requests.get(f"http://localhost:8001/room/{schedule.room_id}")
		locations.append(parse_raw_as(ClassLocation, resp.text))
	
	subjects_today = zip(today, locations)
	
	return templates.TemplateResponse("main.html", {"request": request, "subjects_today": subjects_today})
	#await delete_session(response, session_id)
	
@app.get("/timetable", dependencies=[Depends(cookie)])
def timetable(request: Request, session_data: SessionData = Depends(verifier)):
	response = requests.get(f"http://localhost:8001/schedule/student/{session_data.student_id}")
	response_schedules = parse_raw_as(list[Schedule], response.text)
	
	days = []
	for day in range(5):
		days.append([s for s in response_schedules if s.weekday == day])
		
	days_of_the_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
	
	return templates.TemplateResponse("timetable.html", {"request": request, "days": zip(days, days_of_the_week)})
	
