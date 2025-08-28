from app.database import get_db
from app import models
from sqlalchemy.orm import Session

def fix_existing_administrators():
    """Agrega usuarios administradores existentes a la tabla administradores"""
    db: Session = next(get_db())
    
    # Encontrar todos los usuarios con rol administrador
    admin_users = db.query(models.Usuario).filter(models.Usuario.role == "administrador").all()
    
    print(f"🔍 Encontrados {len(admin_users)} usuarios administradores")
    
    for user in admin_users:
        # Verificar si ya existe en administradores
        existing_admin = db.query(models.Administrador).filter(
            models.Administrador.email == user.email
        ).first()
        
        if not existing_admin:
            # Crear entrada en tabla administradores
            new_admin = models.Administrador(
                email=user.email,
                password_hash=user.password_hash
            )
            db.add(new_admin)
            print(f"✅ Agregado admin: {user.email}")
        else:
            print(f"⚠️  Ya existe en administradores: {user.email}")
    
    db.commit()
    print("🎉 Reparación completada")

if __name__ == "__main__":
    fix_existing_administrators()