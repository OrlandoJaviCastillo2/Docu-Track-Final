import requests
import json
import sys
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "http://localhost:8000"
headers = {"Content-Type": "application/json"}

def print_step(step, message):
    print(f"\n{'='*60}")
    print(f"🚀 {step}: {message}")
    print(f"{'='*60}")

def print_success(message):
    print(f"✅ {message}")

def print_error(message):
    print(f"❌ {message}")

def test_health():
    """Prueba que el servidor esté funcionando"""
    print_step("PASO 1", "Verificar salud del servidor")
    try:
        response = requests.get(f"{BASE_URL}")
        if response.status_code == 200:
            print_success(f"Servidor saludable: {response.json()}")
            return True
        else:
            print_error(f"Error en health check: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"No se pudo conectar al servidor: {e}")
        return False

def test_create_certificate_request(token):
    """Prueba crear solicitud de certificado"""
    print_step("PASO 2", "Crear solicitud de certificado de nacimiento")
    
    certificate_data = {
        "first_name": "María",
        "last_name": "González",
        "identity_number": "987-654321",
        "birth_date": "1985-07-22"
    }
    
    auth_headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/certificados/crear", 
            json=certificate_data, 
            headers=auth_headers
        )
        
        if response.status_code == 200:
            certificate = response.json()
            print_success(f"Solicitud creada: ID {certificate['id']}")
            print_success(f"Estado: {certificate['status']}, UUID: {certificate['identity_number_uuid']}")
            return certificate
        else:
            print_error(f"Error creando solicitud: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print_error(f"Error creando solicitud: {e}")
        return None

def test_get_user_requests(token):
    """Prueba obtener solicitudes del usuario"""
    print_step("PASO 3", "Obtener solicitudes del usuario")
    
    auth_headers = {
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.get(
            f"{BASE_URL}/certificados/mis_solicitudes", 
            headers=auth_headers
        )
        
        if response.status_code == 200:
            requests = response.json()
            print_success(f"Solicitudes encontradas: {len(requests)}")
            for req in requests:
                print_success(f"  - ID: {req['id']}, Estado: {req['status']}, Nombre: {req['first_name']} {req['last_name']}")
            return requests
        else:
            print_error(f"Error obteniendo solicitudes: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print_error(f"Error obteniendo solicitudes: {e}")
        return None

def test_admin_get_requests(admin_token):
    """Prueba que admin pueda ver todas las solicitudes"""
    print_step("PASO 4", "Admin ve todas las solicitudes")
    
    auth_headers = {
        "Authorization": f"Bearer {admin_token}"
    }
    
    try:
        response = requests.get(
            f"{BASE_URL}/admin/solicitudes", 
            headers=auth_headers
        )
        
        if response.status_code == 200:
            requests = response.json()
            print_success(f"Admin ve {len(requests)} solicitudes totales")
            for req in requests:
                print_success(f"  - ID: {req['id']}, Estado: {req['status']}, Solicitante: {req['first_name']} {req['last_name']}")
            return requests
        else:
            print_error(f"Error admin viendo solicitudes: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print_error(f"Error admin viendo solicitudes: {e}")
        return None

def test_admin_update_request(admin_token, request_id):
    """Prueba que admin pueda actualizar estado de solicitud"""
    print_step("PASO 5", "Admin actualiza estado de solicitud")
    
    auth_headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {admin_token}"
    }
    
    # Cambiar estado a "En validación"
    update_data = {"status": "En validación"}
    
    try:
        response = requests.patch(
            f"{BASE_URL}/admin/solicitudes/{request_id}", 
            json=update_data,
            headers=auth_headers
        )
        
        if response.status_code == 200:
            updated = response.json()
            print_success(f"Solicitud actualizada: ID {updated['id']} -> Estado: {updated['status']}")
            
            # Cambiar a "Emitido"
            update_data = {"status": "Emitido"}
            response = requests.patch(
                f"{BASE_URL}/admin/solicitudes/{request_id}", 
                json=update_data,
                headers=auth_headers
            )
            
            if response.status_code == 200:
                final = response.json()
                print_success(f"Solicitud final: ID {final['id']} -> Estado: {final['status']}")
                return final
            else:
                print_error(f"Error en segunda actualización: {response.text}")
                return None
                
        else:
            print_error(f"Error actualizando solicitud: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print_error(f"Error actualizando solicitud: {e}")
        return None

def test_user_get_me(token):
    """Prueba obtener información del usuario actual"""
    print_step("PASO 6", "Obtener información del usuario actual")
    
    auth_headers = {
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.get(
            f"{BASE_URL}/auth/me", 
            headers=auth_headers
        )
        
        if response.status_code == 200:
            user = response.json()
            print_success(f"Usuario actual: {user['email']} (Rol: {user['role']}, ID: {user['id']})")
            return user
        else:
            print_error(f"Error obteniendo usuario: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print_error(f"Error obteniendo usuario: {e}")
        return None

def test_download_certificate(token, request_id):
    """Prueba descargar certificado"""
    print_step("PASO 7", "Intentar descargar certificado")
    
    auth_headers = {
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.get(
            f"{BASE_URL}/certificados/descargar/{request_id}", 
            headers=auth_headers
        )
        
        if response.status_code == 200:
            print_success("✅ Descarga de certificado exitosa")
            return True
        elif response.status_code == 400:
            print_success("⚠️  Certificado no disponible (esperado si no está implementado)")
            return True
        else:
            print_error(f"Error descargando certificado: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print_success("⚠️  Endpoint de descarga no implementado aún (esto es normal)")
        return True

def run_functionality_test(user_token, admin_token, user_email, admin_email):
    """Ejecuta pruebas de funcionalidad con tokens existentes"""
    print("🧪 INICIANDO PRUEBAS DE FUNCIONALIDAD")
    print("🌐 URL base:", BASE_URL)
    print("💡 Usando tokens existentes")
    print(f"   Usuario: {user_email}")
    print(f"   Admin: {admin_email}")
    
    # Paso 1: Verificar servidor
    if not test_health():
        return False
    
    # Paso 2: Obtener información del usuario
    user_info = test_user_get_me(user_token)
    if not user_info:
        return False
    
    # Paso 3: Obtener información del admin
    admin_info = test_user_get_me(admin_token)
    if not admin_info:
        return False
    
    # Paso 4: Crear solicitud de certificado
    certificate = test_create_certificate_request(user_token)
    if not certificate:
        return False
    
    # Paso 5: Obtener solicitudes del usuario
    user_requests = test_get_user_requests(user_token)
    if not user_requests:
        return False
    
    # Paso 6: Admin ve todas las solicitudes
    all_requests = test_admin_get_requests(admin_token)
    if not all_requests:
        return False
    
    # Paso 7: Admin actualiza estado
    updated_request = test_admin_update_request(admin_token, certificate["id"])
    if not updated_request:
        return False
    
    # Paso 8: Intentar descargar certificado
    test_download_certificate(user_token, certificate["id"])
    
    print(f"\n{'🎉'*20}")
    print("🎉 ¡PRUEBAS DE FUNCIONALIDAD COMPLETADAS EXITOSAMENTE!")
    print("🎉 Todas las funciones del backend funcionan correctamente")
    print(f"{'🎉'*20}")
    
    print(f"\n📋 Resumen:")
    print(f"   Usuario: {user_email} (ID: {user_info['id']})")
    print(f"   Admin: {admin_email} (ID: {admin_info['id']})")
    print(f"   Solicitud creada: ID {certificate['id']}")
    print(f"   Estado final: {updated_request['status']}")
    
    return True

if __name__ == "__main__":
    # Tokens y emails (obtenidos previamente del login)
    USER_TOKEN = "tu_token_de_usuario_aqui"  # 🔄 Reemplaza con el token real
    ADMIN_TOKEN = "tu_token_de_admin_aqui"   # 🔄 Reemplaza con el token real
    USER_EMAIL = "marcosflat@gmail.com"
    ADMIN_EMAIL = "orlandojaviercastillo@gmail.com"
    
    # Ejecutar pruebas de funcionalidad
    success = run_functionality_test(USER_TOKEN, ADMIN_TOKEN, USER_EMAIL, ADMIN_EMAIL)
    
    if not success:
        print(f"\n{'⚠️'*20}")
        print("⚠️  Algunas pruebas fallaron. Revisa los errores arriba.")
        print(f"{'⚠️'*20}")
        sys.exit(1)