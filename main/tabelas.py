from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .database import Base

class PacienteDB(Base):
    __tablename__ = "pacientes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    idade = Column(Integer)
    telefone = Column(String)

    consultas = relationship("ConsultaDB", back_populates="paciente")

class ProfissionalDB(Base):
    __tablename__ = "profissionais"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    especialidade = Column(String)

    consultas = relationship("ConsultaDB", back_populates="profissional")

class ConsultaDB(Base):
    __tablename__ = "consultas"

    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"))
    profissional_id = Column(Integer, ForeignKey("profissionais.id"))
    data = Column(DateTime)

    paciente = relationship("PacienteDB", back_populates="consultas")
    profissional = relationship("ProfissionalDB", back_populates="consultas")
