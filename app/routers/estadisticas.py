# app/routers/estadisticas.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.usuario import Usuario
from collections import Counter

router = APIRouter(prefix="/api", tags=["Estadísticas"])

@router.get("/estadisticas")
def estadisticas_usuarios(db: Session = Depends(get_db)):
    usuarios = db.query(Usuario).all()

    total = len(usuarios)

    roles = Counter([u.rol for u in usuarios if u.rol])
    municipios = Counter([u.municipio for u in usuarios if u.municipio])
    etapas = Counter([u.etapa for u in usuarios if u.etapa])
    fincas = set([u.finca for u in usuarios if u.finca])
    productos = set([u.productos for u in usuarios if u.productos])

    # Agrupaciones personalizadas
    productores = [u for u in usuarios if u.rol == "productor"]
    consumidores = [u for u in usuarios if u.rol == "consumidor"]

    productores_por_municipio = Counter([u.municipio for u in productores if u.municipio])
    consumidores_por_municipio = Counter([u.municipio for u in consumidores if u.municipio])
    productores_por_etapa = Counter([u.etapa for u in productores if u.etapa])

    porcentaje_productores = (len(productores) / total) * 100 if total > 0 else 0

    return {
        "total_usuarios": total,
        "roles": roles,
        "productores": len(productores),
        "consumidores": len(consumidores),
        "porcentaje_productores": round(porcentaje_productores, 2),

        "municipios_comunes": municipios.most_common(5),
        "etapas_comunes": etapas.most_common(5),

        "productores_por_municipio": productores_por_municipio,
        "consumidores_por_municipio": consumidores_por_municipio,
        "productores_por_etapa": productores_por_etapa,

        "cantidad_fincas_distintas": len(fincas),
        "cantidad_productos_distintos": len(productos),
    }
