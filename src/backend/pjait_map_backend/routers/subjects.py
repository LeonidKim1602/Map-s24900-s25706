from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import crud
from dependencies import DatabaseManager
from pjait_map_common.schemas import Subject


router = APIRouter(prefix="/subject", dependencies=[Depends(DatabaseManager.get_db)])


@router.get("/")
async def get_subjects(db: Session = Depends(DatabaseManager.get_db)) -> list[Subject]:
    return [Subject(id=s.id, name=s.name) for s in crud.get_subjects(db)]
