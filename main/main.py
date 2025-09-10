from fastapi import FastAPI
from .database import Base, engine
from .routers import pacientes, profissionais, consultas

# Criar tabelas no PostgreSQL
Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Clínica projeto de BD")

# Registrar rotas
app.include_router(pacientes.router)
app.include_router(profissionais.router)
app.include_router(consultas.router)
