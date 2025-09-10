from pydantic import BaseModel
from typing import Optional
from datetime import date, time, datetime

# Paciente
class PacienteBase(BaseModel):
    nome: str
    data_nascimento: date
    cpf: str
    telefone: str

class PacienteCreate(PacienteBase):
    pass

class PacienteOut(PacienteBase):
    id: int
    class Config:
        from_attributes = True

# Profissional
class ProfissionalBase(BaseModel):
    nome: str
    especialidade: str
    registro: str
    telefone: Optional[str] = None

class ProfissionalCreate(ProfissionalBase):
    pass

class ProfissionalOut(ProfissionalBase):
    id: int
    class Config:
        from_attributes = True

# Consulta
class ConsultaBase(BaseModel):
    paciente_id: int
    profissional_id: int
    data: date
    hora: time

class ConsultaCreate(ConsultaBase):
    pass

class ConsultaOut(ConsultaBase):
    id: int
    class Config:
        from_attributes = True