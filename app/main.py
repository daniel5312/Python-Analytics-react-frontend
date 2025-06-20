# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import Base, engine
from app.routers import usuarios
from app.routers import estadisticas# # 👈 Asegúrate de importar estadisticas
from app.routers import productos_productor

app = FastAPI()

# Crear las tablas si no existen
Base.metadata.create_all(bind=engine)

# Habilitar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(usuarios.router)
app.include_router(estadisticas.router)
