# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import Base, engine
from app.routers import usuarios
from app.routers import estadisticas# 👈 Asegúrate de importar estadisticas

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 📌 Registrar routers
app.include_router(usuarios.router)
app.include_router(estadisticas.router)  # 👈 Aquí lo agregas
