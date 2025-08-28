from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import uuid
from app.database import get_db
from app.models import SolicitudCertificado
from app.schemas import SolicitudCreate, SolicitudResponse
from app.auth.get_current_user import get_current_user
from fastapi.responses import FileResponse
import os
from ..auth.utils import generar_pdf_certificado  # Importar la función de generación de PDF


router = APIRouter()

@router.post("/crear", response_model=SolicitudResponse)
def crear_solicitud(
    solicitud: SolicitudCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"] != "usuario":
        raise HTTPException(status_code=403, detail="Solo usuarios pueden crear solicitudes")

    try:
        solicitud_uuid = str(uuid.uuid4())
        usuario = current_user["user"]
        
        nueva_solicitud = SolicitudCertificado(
            first_name=solicitud.first_name,
            last_name=solicitud.last_name,
            identity_number=solicitud.identity_number,
            birth_date=solicitud.birth_date,
            status="Recibido",
            identity_number_uuid=solicitud_uuid,
            user_id=usuario.id,
        )
        
        db.add(nueva_solicitud)
        db.commit()
        db.refresh(nueva_solicitud)
        return nueva_solicitud
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/mis_solicitudes", response_model=List[SolicitudResponse])
def listar_mis_solicitudes(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"] != "usuario":
        raise HTTPException(status_code=403, detail="Solo usuarios pueden ver solicitudes")
    
    usuario = current_user["user"]
    return db.query(SolicitudCertificado).filter_by(user_id=usuario.id).all()


@router.get("/descargar/{solicitud_id}")
def descargar_certificado(
    solicitud_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Descarga un certificado en PDF"""
    if current_user["role"] != "usuario":
        raise HTTPException(status_code=403, detail="Solo usuarios pueden descargar certificados")
    
    # Buscar la solicitud
    solicitud = db.query(SolicitudCertificado).filter(
        SolicitudCertificado.id == solicitud_id,
        SolicitudCertificado.user_id == current_user["user"].id
    ).first()
    
    if not solicitud:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")
    
    if solicitud.status != "Emitido":
        raise HTTPException(status_code=400, detail="El certificado no está disponible para descarga")
    
    # Generar certificado si no existe o si es un archivo antiguo (txt/html)
    if (not solicitud.file_path or 
        not os.path.exists(solicitud.file_path) or
        not solicitud.file_path.endswith('.pdf')):
        
        file_path = generar_pdf_certificado({
            'id': solicitud.id,
            'first_name': solicitud.first_name,
            'last_name': solicitud.last_name,
            'identity_number': solicitud.identity_number,
            'birth_date': solicitud.birth_date.strftime("%d/%m/%Y"),
            'identity_number_uuid': solicitud.identity_number_uuid,
            'status': solicitud.status
        })
        
        if not file_path:
            raise HTTPException(status_code=500, detail="Error generando certificado")
        
        # Si se generó un archivo de texto como fallback, lo convertimos a PDF
        if file_path.endswith('.txt'):
            # Forzar regeneración hasta obtener PDF
            file_path = generar_pdf_certificado({
                'id': solicitud.id,
                'first_name': solicitud.first_name,
                'last_name': solicitud.last_name,
                'identity_number': solicitud.identity_number,
                'birth_date': solicitud.birth_date.strftime("%d/%m/%Y"),
                'identity_number_uuid': solicitud.identity_number_uuid,
                'status': solicitud.status
            })
        
        solicitud.file_path = file_path
        db.commit()
    
    # Verificar que el archivo existe y es PDF
    if not os.path.exists(solicitud.file_path):
        raise HTTPException(status_code=500, detail="Archivo de certificado no encontrado")
    
    # Siempre devolvemos como PDF
    filename = f"certificado_{solicitud.first_name}_{solicitud.last_name}.pdf"
    
    return FileResponse(
        solicitud.file_path,
        filename=filename,
        media_type="application/pdf"
    )


@router.get("/emitidos", response_model=List[SolicitudResponse])
def obtener_certificados_emitidos(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Obtiene solo los certificados emitidos del usuario"""
    if current_user["role"] != "usuario":
        raise HTTPException(status_code=403, detail="Solo usuarios pueden ver certificados")
    
    return db.query(SolicitudCertificado).filter(
        SolicitudCertificado.user_id == current_user["user"].id,
        SolicitudCertificado.status == "Emitido"
    ).all()