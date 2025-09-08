from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/consultas", tags=["Consultas"])

@router.post("/", response_model=schemas.ConsultaOut)
def criar_consulta(consulta: schemas.ConsultaCreate, db: Session = Depends(get_db)):
    db_consulta = models.ConsultaDB(**consulta.dict())
    db.add(db_consulta)
    db.commit()
    db.refresh(db_consulta)
    return db_consulta

@router.get("/", response_model=List[schemas.ConsultaOut])
def listar_consultas(db: Session = Depends(get_db)):
    return db.query(models.ConsultaDB).all()
