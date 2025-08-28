from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.auth.routes import auth_router
from app.certificados.routes import router as certificados_router
from app.admin.routes import admin_router

# Crear tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI(title="DocuTrack API", version="1.0.0")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Bienvenido a DocuTrack API"}

# Incluir routers
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(certificados_router, prefix="/certificados", tags=["certificados"])
app.include_router(admin_router, prefix="/admin", tags=["admin"])

@app.get("/health")
def health_check():
    return {"status": "healthy", "database": "connected"}