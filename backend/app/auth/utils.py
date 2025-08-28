from fastapi import HTTPException, status
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
import os
from dotenv import load_dotenv
from jinja2 import Template

load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", 60))

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

def generar_pdf_certificado(solicitud_data):
    """Genera un PDF real del certificado usando WeasyPrint"""
    try:
        # Template HTML profesional (mantenemos el mismo)
        template_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Certificado de Nacimiento</title>
            <style>
                body { 
                    font-family: Arial, sans-serif; 
                    margin: 40px;
                    color: #333;
                }
                .header { 
                    text-align: center; 
                    margin-bottom: 30px;
                    border-bottom: 2px solid #333;
                    padding-bottom: 20px;
                }
                .title { 
                    font-size: 24px; 
                    font-weight: bold;
                    color: #2c5aa0;
                }
                .content { 
                    font-size: 16px; 
                    line-height: 1.8;
                    margin: 20px 0;
                }
                .field { 
                    margin-bottom: 15px;
                    display: flex;
                }
                .label { 
                    font-weight: bold; 
                    width: 200px;
                    color: #555;
                }
                .footer { 
                    margin-top: 50px; 
                    text-align: center; 
                    font-size: 14px; 
                    color: #666;
                    border-top: 1px solid #ccc;
                    padding-top: 20px;
                }
                .seal {
                    text-align: center;
                    margin: 30px 0;
                }
                .uuid {
                    font-family: monospace;
                    background-color: #f5f5f5;
                    padding: 5px;
                    border-radius: 4px;
                }
            </style>
        </head>
        <body>
            <div class="header">
                <div class="title">CERTIFICADO DE NACIMIENTO</div>
                <div>Documento Oficial - República de DocuTrack</div>
            </div>
            
            <div class="content">
                <div class="field">
                    <span class="label">Nombre completo:</span>
                    <span>{{nombre_completo}}</span>
                </div>
                <div class="field">
                    <span class="label">Número de identidad:</span>
                    <span>{{identity_number}}</span>
                </div>
                <div class="field">
                    <span class="label">Fecha de nacimiento:</span>
                    <span>{{birth_date}}</span>
                </div>
                <div class="field">
                    <span class="label">UUID del certificado:</span>
                    <span class="uuid">{{identity_number_uuid}}</span>
                </div>
                <div class="field">
                    <span class="label">Fecha de emisión:</span>
                    <span>{{fecha_emision}}</span>
                </div>
                <div class="field">
                    <span class="label">Estado:</span>
                    <span>{{status}}</span>
                </div>
            </div>
            
            <div class="seal">
                <div style="font-size: 18px; font-weight: bold; margin-bottom: 10px;">
                    DOCUMENTO OFICIAL VÁLIDO
                </div>
                <div>_________________________________</div>
                <div>Firma y sello electrónico</div>
                <div>DocuTrack - Sistema de Certificados Digitales</div>
            </div>
            
            <div class="footer">
                <p>Este es un documento oficial emitido electrónamente.</p>
                <p>UUID: {{identity_number_uuid}} | Emitido el: {{fecha_emision}}</p>
                <p>Verificar en: http://localhost:8000/verificar/{{identity_number_uuid}}</p>
            </div>
        </body>
        </html>
        """
        
        # Renderizar template
        template = Template(template_html)
        html_content = template.render({
            'nombre_completo': f"{solicitud_data['first_name']} {solicitud_data['last_name']}",
            'identity_number': solicitud_data['identity_number'],
            'birth_date': solicitud_data['birth_date'],
            'identity_number_uuid': solicitud_data['identity_number_uuid'],
            'status': solicitud_data['status'],
            'fecha_emision': datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        })
        
        # Crear directorio
        os.makedirs("certificados", exist_ok=True)
        pdf_path = f"certificados/certificado_{solicitud_data['id']}.pdf"
        
        # Usar WeasyPrint en lugar de pdfkit
        from weasyprint import HTML
        HTML(string=html_content).write_pdf(pdf_path)
        
        return pdf_path
        
    except Exception as e:
        print(f"Error generando PDF con WeasyPrint: {e}")
        # Fallback a texto (mantenemos el mismo)
        return generar_certificado_texto(solicitud_data)

def generar_certificado_texto(solicitud_data):
    """Fallback: generar certificado en texto (sin cambios)"""
    try:
        os.makedirs("certificados", exist_ok=True)
        txt_path = f"certificados/certificado_{solicitud_data['id']}.txt"
        
        contenido = f"""
{'='*60}
CERTIFICADO DE NACIMIENTO - DOCUMENTO OFICIAL
{'='*60}

INFORMACIÓN DEL TITULAR:
• Nombre completo: {solicitud_data['first_name']} {solicitud_data['last_name']}
• Número de identidad: {solicitud_data['identity_number']}
• Fecha de nacimiento: {solicitud_data['birth_date']}

INFORMACIÓN DEL CERTIFICADO:
• UUID: {solicitud_data['identity_number_uuid']}
• Estado: {solicitud_data['status']}
• Fecha de emisión: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}

{'='*60}
DOCUMENTO VÁLIDO PARA TRÁMITES OFICIALES
Sistema DocuTrack - Certificación Digital
{'='*60}
        """
        
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write(contenido)
        
        return txt_path
        
    except Exception as e:
        print(f"Error en fallback texto: {e}")
        return None