from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/profissionais", tags=["Profissionais"])

@router.post("/", response_model=schemas.ProfissionalOut)
def criar_profissional(profissional: schemas.ProfissionalCreate, db: Session = Depends(get_db)):
    db_prof = models.ProfissionalDB(**profissional.dict())
    db.add(db_prof)
    db.commit()
    db.refresh(db_prof)
    return db_prof

@router.get("/", response_model=List[schemas.ProfissionalOut])
def listar_profissionais(db: Session = Depends(get_db)):
    return db.query(models.ProfissionalDB).all()
