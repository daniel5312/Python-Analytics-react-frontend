# app/models/producto.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import relationship
from datetime import date
from app.db.database import Base

class Producto(Base):
    __tablename__ = "productos_productor"  # nombre de la tabla en la base de datos

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)  # nombre del producto
    descripcion = Column(String(255))             # descripción opcional
    precio = Column(Float, nullable=False)        # precio obligatorio
    imagen = Column(String(255))                  # URL de imagen
    categoria = Column(String(50))                # fruta, hortaliza, etc
    fecha = Column(Date, default=date.today)      # fecha de publicación

    productor_id = Column(Integer, ForeignKey("usuarios.id"))
    productor = relationship("Usuario", back_populates="productos_relacion")# relación ORM