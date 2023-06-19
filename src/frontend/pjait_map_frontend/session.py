from pydantic import BaseModel
from fastapi import HTTPException, FastAPI, Response, Depends
from uuid import UUID, uuid4

from fastapi_sessions.backends.implementations import InMemoryBackend
from fastapi_sessions.session_verifier import SessionVerifier
from fastapi_sessions.frontends.implementations import SessionCookie, CookieParameters


class SessionData(BaseModel):
    student_id: int


cookie_params = CookieParameters()

# Uses UUID
cookie = SessionCookie(
    cookie_name="session",
    identifier="general_verifier",
    auto_error=True,
    secret_key="DONOTUSE",
    cookie_params=cookie_params,
)
backend = InMemoryBackend[UUID, SessionData]()

async def create_session(response, data):
	session = uuid4()
	
	await backend.create(session, data)
	cookie.attach_to_response(response, session)

async def delete_session(response, session_id):
	await backend.delete(session_id)
	cookie.delete_from_response(response)

