from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.auth.utils import get_password_hash, verify_password, create_access_token
from app.auth.get_current_user import get_current_user

auth_router = APIRouter()

@auth_router.post("/register", response_model=schemas.UserOut)
def register_user(payload: schemas.RegistroRequest, db: Session = Depends(get_db)):
    existing_user = (
        db.query(models.Usuario)
        .filter(models.Usuario.email == payload.email)
        .first()
    )
    if existing_user:
        raise HTTPException(status_code=400, detail="Correo ya registrado")

    hashed_password = get_password_hash(payload.password)  
    new_user = models.Usuario(
        email=payload.email,
        password_hash=hashed_password,
        full_name=payload.full_name,
        role=payload.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    #Si es administrador, también agregar a tabla administradores
    if payload.role == "administrador":
        new_admin = models.Administrador(
            id = new_user.id,
            email=payload.email,
            password_hash=hashed_password  # Mismo hash de contraseña
        )
        db.add(new_admin)
        db.commit()

    return new_user

@auth_router.post("/login")
def login_user(payload: schemas.LoginRequest, db: Session = Depends(get_db)):
    # Buscar usuario o administrador
    usuario = db.query(models.Usuario).filter(models.Usuario.email == payload.email).first()
    admin = db.query(models.Administrador).filter(models.Administrador.email == payload.email).first()

    user = usuario or admin
    role = "usuario" if usuario else "administrador" if admin else None

    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    # Crear token JWT
    token = create_access_token({
        "sub": str(user.id),
        "email": user.email,
        "role": user.role
    })

    return JSONResponse(content={
        "access_token": token,
        "token_type": "bearer",
        "role": user.role,
        "user_id": user.id
    })

@auth_router.get("/me", response_model=schemas.UserOut)
def get_me(
    current_user_data: dict = Depends(get_current_user)
):
    user = current_user_data["user"]
    role = current_user_data["role"]
    
    # Para administradores, se adapta respuesta compatible con UserOut
    if role == "administrador":
        # Los administradores no tienen todos los campos de User,se necesitaadaptar
        return {
            "id": user.id,
            "email": user.email,
            "role": role,
            "full_name": getattr(user, 'full_name', 'Administrador')  # Campo opcional
        }
    else:
        # Para usuarios normales, devolver directamente
        return user