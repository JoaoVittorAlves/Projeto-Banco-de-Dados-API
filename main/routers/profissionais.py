from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from sqlalchemy import text
from starlette import status
from typing import List, Optional
from ..database import get_db
from .. import schemas, tabelas as models

router = APIRouter(prefix="/profissionais", tags=["Profissionais"])

@router.post("/", response_model=schemas.ProfissionalOut)
def criar_profissional(profissional: schemas.ProfissionalCreate, db: Session = Depends(get_db)):
    query = text("""
        INSERT INTO profissional (nome, especialidade, registro, telefone) 
        VALUES (:nome, :especialidade, :registro, :telefone)
        RETURNING id, nome, especialidade, registro, telefone
    """)
    result = db.execute(query, profissional.dict()).first()
    db.commit()
    if result is None:
        raise HTTPException(status_code=500, detail="Erro ao criar o profissional")
    return dict(result._mapping)

@router.get("/", response_model=List[schemas.ProfissionalOut])
def listar_profissionais(db: Session = Depends(get_db), nome: Optional[str] = None):
    base_query = "SELECT id, nome, especialidade, registro, telefone FROM profissional"
    params = {}
    if nome:
        base_query += " WHERE nome ILIKE :nome"
        params["nome"] = f"%{nome}%"
    
    query = text(base_query)
    result = db.execute(query, params).fetchall()
    profissionais = [dict(row._mapping) for row in result]
    return profissionais

@router.get("/{profissional_id}", response_model=schemas.ProfissionalOut)
def ler_profissional_por_id(profissional_id: int, db: Session = Depends(get_db)):
    query = text("SELECT id, nome, especialidade, registro, telefone FROM profissional WHERE id = :id")
    result = db.execute(query, {"id": profissional_id}).first()
    if result is None:
        raise HTTPException(status_code=404, detail="Profissional não encontrado")
    return dict(result._mapping)

@router.put("/{profissional_id}", response_model=schemas.ProfissionalOut)
def atualizar_profissional(profissional_id: int, profissional: schemas.ProfissionalCreate, db: Session = Depends(get_db)):
    query = text("""
        UPDATE profissional 
        SET nome = :nome, especialidade = :especialidade, registro = :registro, telefone = :telefone
        WHERE id = :id
        RETURNING id, nome, especialidade, registro, telefone
    """)
    params = profissional.dict()
    params["id"] = profissional_id
    result = db.execute(query, params).first()
    db.commit()
    if result is None:
        raise HTTPException(status_code=404, detail="Profissional não encontrado para atualização")
    return dict(result._mapping)

@router.delete("/{profissional_id}", status_code=status.HTTP_204_NO_CONTENT)
def remover_profissional(profissional_id: int, db: Session = Depends(get_db)):
    check_query = text("SELECT id FROM profissional WHERE id = :id")
    profissional_existe = db.execute(check_query, {"id": profissional_id}).first()
    if profissional_existe is None:
        raise HTTPException(status_code=404, detail="Profissional não encontrado")

    delete_query = text("DELETE FROM profissional WHERE id = :id")
    db.execute(delete_query, {"id": profissional_id})
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)