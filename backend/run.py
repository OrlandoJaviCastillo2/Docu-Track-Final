import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",    # Ruta al módulo: app.main y la variable app
        host="0.0.0.0",    # Escuchar en todas las interfaces
        port=8000,         # Puerto 8000
        reload=True        # Recarga automática al hacer cambios
    )