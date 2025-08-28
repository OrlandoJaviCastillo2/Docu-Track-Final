import os
from app.auth.utils import generar_pdf_certificado

# Datos de prueba
solicitud_data = {
    'id': 1,
    'first_name': 'Carlos',
    'last_name': 'Rodríguez', 
    'identity_number': '123-987654',
    'birth_date': '1992-11-15',
    'identity_number_uuid': 'a1b2c3d4-e5f6-7890',
    'status': 'Emitido'
}

print("🧪 Probando generación de PDF...")
print("📋 Datos:", solicitud_data)

# Probar generar PDF
resultado = generar_pdf_certificado(solicitud_data)
print("📄 Resultado:", resultado)

# Verificar si el archivo existe
if resultado and os.path.exists(resultado):
    print("✅ Archivo creado exitosamente")
    print("📊 Tamaño:", os.path.getsize(resultado), "bytes")
else:
    print("❌ Error creando archivo")
    print("💡 Verifica la instalación de wkhtmltopdf")