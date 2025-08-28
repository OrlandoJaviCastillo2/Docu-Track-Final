from pydantic import BaseModel, EmailStr, Field
from typing import Literal, Optional
from datetime import date, datetime

class RegistroRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)
    full_name: str = Field(..., min_length=2)
    role: Literal["usuario", "administrador"] = "usuario"

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class SolicitudCreate(BaseModel):
    first_name: str = Field(..., min_length=1)
    last_name: str = Field(..., min_length=1)
    identity_number: str = Field(..., pattern=r'^[0-9\-]+$')
    birth_date: date

class SolicitudResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    identity_number: str
    birth_date: date
    status: str
    identity_number_uuid: str
    requested_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class StatusUpdate(BaseModel):
    status: Literal["Recibido", "En validación", "Rechazado", "Emitido"]

class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: str
    full_name: Optional[str] = None  
    
    class Config:
        from_attributes = True
    
    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    role: str
    user_id: int