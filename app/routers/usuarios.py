from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioLogin
from app.schemas.usuario import UsuarioCreate, UsuarioOut

router = APIRouter(prefix="/api/usuarios", tags=["Usuarios"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
@router.get("/estadisticas")
def estadisticas_usuarios(db: Session = Depends(SessionLocal)):
    usuarios = db.query(Usuario).all()

    total = len(usuarios)
    roles = Counter([u.rol for u in usuarios if u.rol])
    municipios = Counter([u.municipio for u in usuarios if u.municipio])
    etapas = Counter([u.etapa for u in usuarios if u.etapa])

    return {
        "total_usuarios": total,
        "productores": roles.get("productor", 0),
        "consumidores": roles.get("consumidor", 0),
        "municipios_comunes": municipios.most_common(3),
        "etapas_comunes": etapas.most_common(3),
    }

@router.post("/register", response_model=UsuarioOut)
def register_user(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    db_usuario = db.query(Usuario).filter(Usuario.email == usuario.email).first()
    if db_usuario:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")
    nuevo_usuario = Usuario(**usuario.dict())
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario

@router.post("/login", response_model=UsuarioOut)
def login_usuario(datos: UsuarioLogin, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == datos.email).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if usuario.password != datos.password:
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")

    return usuario
@router.get("/", response_model=list[UsuarioOut])
def listar_usuarios(db: Session = Depends(get_db)):
    return db.query(Usuario).all()

@router.get("/{id}", response_model=UsuarioOut)
def obtener_usuario(id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@router.put("/{id}", response_model=UsuarioOut)
def actualizar_usuario(id: int, datos: UsuarioCreate, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    for key, value in datos.dict().items():
        setattr(usuario, key, value)

    db.commit()
    db.refresh(usuario)
    return usuario

# Eliminar usuario por ID
@router.delete("/{id}")
def eliminar_usuario(id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    db.delete(usuario)
    db.commit()
    return {"mensaje": f"Usuario con ID {id} eliminado correctamente"}

