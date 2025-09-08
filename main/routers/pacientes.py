from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from main.database import get_db
from main.models import Paciente
from main.schemas import PacienteCreate


router = APIRouter(prefix="/pacientes", tags=["Pacientes"])

@router.post("/", response_model=schemas.PacienteOut)
def criar_paciente(paciente: schemas.PacienteCreate, db: Session = Depends(get_db)):
    db_paciente = models.PacienteDB(**paciente.dict())
    db.add(db_paciente)
    db.commit()
    db.refresh(db_paciente)
    return db_paciente

@router.get("/", response_model=List[schemas.PacienteOut])
def listar_pacientes(db: Session = Depends(get_db)):
    return db.query(models.PacienteDB).all()
