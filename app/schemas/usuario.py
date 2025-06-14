from pydantic import BaseModel

# Esquema para registro de usuario
class UsuarioCreate(BaseModel):
    nombre: str
    email: str
    password: str
    rol: str
    finca: str | None = None
    municipio: str | None = None
    vereda: str | None = None
    productos: str | None = None
    etapa: str | None = None

# Esquema para respuesta (al mostrar un usuario)
class UsuarioOut(BaseModel):
    id: int
    nombre: str
    email: str
    rol: str
    finca: str | None = None
    municipio: str | None = None
    vereda: str | None = None
    productos: str | None = None
    etapa: str | None = None

    class Config:
        orm_mode = True

# Esquema para login
class UsuarioLogin(BaseModel):
    email: str
    password: str
