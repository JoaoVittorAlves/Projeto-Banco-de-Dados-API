from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Date, Numeric
from sqlalchemy.orm import relationship
from .database import Base


class PacienteDB(Base):
    __tablename__ = "pacientes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    data_nascimento = Column(Date)
    cpf = Column(String, unique=True, index=True, nullable=False)
    telefone = Column(String)

    consultas = relationship("ConsultaDB", back_populates="paciente")

class ProfissionalDB(Base):
    __tablename__ = "profissionais"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    especialidade = Column(String)
    registro = Column(String, unique=True)

    consultas = relationship("ConsultaDB", back_populates="profissional")

class ConsultaDB(Base):
    __tablename__ = "consultas"

    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"))
    profissional_id = Column(Integer, ForeignKey("profissionais.id"))
    data = Column(DateTime)
    status = Column(String, default="Agendada")
    valor_consulta = Column(Numeric(10, 2))

    paciente = relationship("PacienteDB", back_populates="consultas")
    profissional = relationship("ProfissionalDB", back_populates="consultas")
