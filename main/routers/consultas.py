from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from sqlalchemy import text
from starlette import status
from typing import List, Optional
from ..database import get_db
from .. import schemas, tabelas as models

router = APIRouter(prefix="/consultas", tags=["Consultas"])

@router.post("/", response_model=schemas.ConsultaOut)
def criar_consulta(consulta: schemas.ConsultaCreate, db: Session = Depends(get_db)):
    query = text("""
        INSERT INTO consulta (data, hora, paciente_id, profissional_id) 
        VALUES (:data, :hora, :paciente_id, :profissional_id)
        RETURNING id, data, hora, paciente_id, profissional_id
    """)
    result = db.execute(query, consulta.dict()).first()
    db.commit()
    if result is None:
        raise HTTPException(status_code=500, detail="Erro ao criar a consulta")
    return dict(result._mapping)

@router.get("/", response_model=List[schemas.ConsultaOut])
def listar_consultas(db: Session = Depends(get_db)):
    query = text("SELECT id, data, hora, paciente_id, profissional_id FROM consulta")
    result = db.execute(query).fetchall()
    consultas = [dict(row._mapping) for row in result]
    return consultas

@router.get("/{consulta_id}", response_model=schemas.ConsultaOut)
def ler_consulta_por_id(consulta_id: int, db: Session = Depends(get_db)):
    query = text("SELECT id, data, hora, paciente_id, profissional_id FROM consulta WHERE id = :id")
    result = db.execute(query, {"id": consulta_id}).first()
    if result is None:
        raise HTTPException(status_code=404, detail="Consulta não encontrada")
    return dict(result._mapping)

@router.put("/{consulta_id}", response_model=schemas.ConsultaOut)
def atualizar_consulta(consulta_id: int, consulta: schemas.ConsultaCreate, db: Session = Depends(get_db)):
    query = text("""
        UPDATE consulta 
        SET data = :data, hora = :hora, paciente_id = :paciente_id, profissional_id = :profissional_id
        WHERE id = :id
        RETURNING id, data, hora, paciente_id, profissional_id
    """)
    params = consulta.dict()
    params["id"] = consulta_id
    result = db.execute(query, params).first()
    db.commit()
    if result is None:
        raise HTTPException(status_code=404, detail="Consulta não encontrada para atualização")
    return dict(result._mapping)

@router.delete("/{consulta_id}", status_code=status.HTTP_204_NO_CONTENT)
def remover_consulta(consulta_id: int, db: Session = Depends(get_db)):
    check_query = text("SELECT id FROM consulta WHERE id = :id")
    consulta_existe = db.execute(check_query, {"id": consulta_id}).first()
    if consulta_existe is None:
        raise HTTPException(status_code=404, detail="Consulta não encontrada")

    delete_query = text("DELETE FROM consulta WHERE id = :id")
    db.execute(delete_query, {"id": consulta_id})
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)