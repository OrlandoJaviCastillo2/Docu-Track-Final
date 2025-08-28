from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text, TIMESTAMP, CheckConstraint, DateTime, func
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    full_name = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    role = Column(String, default="usuario")  

    certificados = relationship("SolicitudCertificado", back_populates="usuario")

class Administrador(Base):
    __tablename__ = "administradores"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

class SolicitudCertificado(Base):
    __tablename__ = "solicitud_certificados"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"))
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    identity_number = Column(String(30), nullable=False)
    identity_number_uuid = Column(String(36), unique=True, nullable=False)
    birth_date = Column(Date, nullable=False)
    status = Column(String(20), nullable=False, default="Recibido")
    file_path = Column(Text)
    requested_at = Column(TIMESTAMP, server_default=func.now())
                             
    __table_args__ = (
        CheckConstraint("identity_number ~ '^[0-9\\-]+$'", name="identity_number_format"),
        CheckConstraint("status IN ('Recibido', 'En validación', 'Rechazado', 'Emitido')", name="valid_status"),
    )

    usuario = relationship("Usuario", back_populates="certificados")