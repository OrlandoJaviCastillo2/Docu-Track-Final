from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas
from app.auth.get_current_user import get_current_user
from app.database import get_db

admin_router = APIRouter()

@admin_router.get("/solicitudes", response_model=List[schemas.SolicitudResponse])
def admin_listar_solicitudes(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user["role"] != "administrador":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    
    return db.query(models.SolicitudCertificado).all()

@admin_router.patch("/solicitudes/{solicitud_id}", response_model=schemas.SolicitudResponse)
def cambiar_estado_solicitud(
    solicitud_id: int, 
    payload: schemas.StatusUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user["role"] != "administrador":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    
    solicitud = db.query(models.SolicitudCertificado).filter_by(id=solicitud_id).first()
    if not solicitud:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    solicitud.status = payload.status
    db.commit()
    db.refresh(solicitud)
    
    return solicitud