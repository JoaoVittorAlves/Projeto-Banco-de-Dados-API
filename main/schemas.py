from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Paciente
class PacienteBase(BaseModel):
    nome: str
    idade: int
    telefone: str

class PacienteCreate(PacienteBase):
    pass

class PacienteOut(PacienteBase):
    id: int
    class Config:
        orm_mode = True

# Profissional
class ProfissionalBase(BaseModel):
    nome: str
    especialidade: str

class ProfissionalCreate(ProfissionalBase):
    pass

class ProfissionalOut(ProfissionalBase):
    id: int
    class Config:
        orm_mode = True

# Consulta
class ConsultaBase(BaseModel):
    paciente_id: int
    profissional_id: int
    data: datetime

class ConsultaCreate(ConsultaBase):
    pass

class ConsultaOut(ConsultaBase):
    id: int
    class Config:
        orm_mode = True
