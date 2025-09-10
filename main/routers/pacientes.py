from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from sqlalchemy import text
from starlette import status
from typing import List, Optional
from ..database import get_db
from .. import schemas, tabelas as models

router = APIRouter(prefix="/pacientes", tags=["Pacientes"])

@router.post("/", response_model=schemas.PacienteOut)
def criar_paciente(paciente: schemas.PacienteCreate, db: Session = Depends(get_db)):
    query = text("""
        INSERT INTO paciente (nome, data_nascimento, cpf, telefone) 
        VALUES (:nome, :data_nascimento, :cpf, :telefone)
        RETURNING id, nome, data_nascimento, cpf, telefone
    """)
    result = db.execute(query, paciente.dict()).first()
    db.commit()
    if result is None:
        raise HTTPException(status_code=500, detail="Erro ao criar o paciente")
    return dict(result._mapping)

@router.get("/", response_model=List[schemas.PacienteOut])
def listar_pacientes(db: Session = Depends(get_db), nome: Optional[str] = None):
    base_query = "SELECT id, nome, data_nascimento, cpf, telefone FROM paciente"
    params = {}
    if nome:
        base_query += " WHERE nome ILIKE :nome"
        params["nome"] = f"%{nome}%"
    
    query = text(base_query)
    result = db.execute(query, params).fetchall()
    pacientes = [dict(row._mapping) for row in result]
    return pacientes

@router.get("/{paciente_id}", response_model=schemas.PacienteOut)
def ler_paciente_por_id(paciente_id: int, db: Session = Depends(get_db)):
    query = text("SELECT id, nome, data_nascimento, cpf, telefone FROM paciente WHERE id = :id")
    result = db.execute(query, {"id": paciente_id}).first()
    if result is None:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    return dict(result._mapping)

@router.put("/{paciente_id}", response_model=schemas.PacienteOut)
def atualizar_paciente(paciente_id: int, paciente: schemas.PacienteCreate, db: Session = Depends(get_db)):
    query = text("""
        UPDATE paciente 
        SET nome = :nome, data_nascimento = :data_nascimento, cpf = :cpf, telefone = :telefone
        WHERE id = :id
        RETURNING id, nome, data_nascimento, cpf, telefone
    """)
    params = paciente.dict()
    params["id"] = paciente_id
    result = db.execute(query, params).first()
    db.commit()
    if result is None:
        raise HTTPException(status_code=404, detail="Paciente não encontrado para atualização")
    return dict(result._mapping)

@router.delete("/{paciente_id}", status_code=status.HTTP_204_NO_CONTENT)
def remover_paciente(paciente_id: int, db: Session = Depends(get_db)):
    check_query = text("SELECT id FROM paciente WHERE id = :id")
    paciente_existe = db.execute(check_query, {"id": paciente_id}).first()
    if paciente_existe is None:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    
    delete_query = text("DELETE FROM paciente WHERE id = :id")
    db.execute(delete_query, {"id": paciente_id})
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)