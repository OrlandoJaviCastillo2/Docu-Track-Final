import requests
import sys
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "http://localhost:8000"
headers = {"Content-Type": "application/json"}

def print_step(message):
    print(f"\n{'='*50}")
    print(f"🚀 {message}")
    print(f"{'='*50}")

def print_success(message):
    print(f"✅ {message}")

def print_error(message):
    print(f"❌ {message}")

def test_login_usuario():
    """Prueba login de usuario normal"""
    print_step("1. LOGIN DE USUARIO")
    
    login_data = {
        "email": "marcosflat@gmail.com",
        "password": "muri1234"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            print_success(f"Login exitoso!")
            print_success(f"Email: {data.get('email', 'N/A')}")
            print_success(f"Rol: {data.get('role', 'N/A')}")
            print_success(f"User ID: {data.get('user_id', 'N/A')}")
            print_success(f"Token: {data['access_token'][:30]}...")
            return data
        else:
            print_error(f"Error en login: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print_error(f"Error de conexión: {e}")
        return None

def test_crear_solicitud(token):
    """Prueba crear solicitud de certificado"""
    print_step("2. CREAR SOLICITUD DE CERTIFICADO")
    
    certificate_data = {
        "first_name": "Carlos",
        "last_name": "Rodríguez",
        "identity_number": "123-987654",
        "birth_date": "1992-11-15"
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
            print_success(f"Solicitud creada exitosamente!")
            print_success(f"ID: {certificate['id']}")
            print_success(f"Estado: {certificate['status']}")
            print_success(f"UUID único: {certificate['identity_number_uuid']}")
            print_success(f"Nombre: {certificate['first_name']} {certificate['last_name']}")
            return certificate
        else:
            print_error(f"Error creando solicitud: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print_error(f"Error creando solicitud: {e}")
        return None

def test_ver_mis_solicitudes(token):
    """Prueba ver solicitudes del usuario"""
    print_step("3. VER MIS SOLICITUDES")
    
    auth_headers = {
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.get(
            f"{BASE_URL}/certificados/mis_solicitudes", 
            headers=auth_headers
        )
        
        if response.status_code == 200:
            solicitudes = response.json()
            print_success(f"Tienes {len(solicitudes)} solicitud(es):")
            
            for i, solicitud in enumerate(solicitudes, 1):
                print_success(f"{i}. ID: {solicitud['id']}")
                print_success(f"   Nombre: {solicitud['first_name']} {solicitud['last_name']}")
                print_success(f"   Cédula: {solicitud['identity_number']}")
                print_success(f"   Estado: {solicitud['status']}")
                print_success(f"   Fecha: {solicitud.get('requested_at', 'N/A')}")
                print_success(f"   UUID: {solicitud['identity_number_uuid']}")
                print("   " + "-"*40)
            
            return solicitudes
        else:
            print_error(f"Error obteniendo solicitudes: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print_error(f"Error obteniendo solicitudes: {e}")
        return None

def test_ver_mi_informacion(token):
    """Prueba ver información del usuario"""
    print_step("4. VER MI INFORMACIÓN")
    
    auth_headers = {
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.get(
            f"{BASE_URL}/auth/me", 
            headers=auth_headers
        )
        
        if response.status_code == 200:
            usuario = response.json()
            print_success("Información del usuario:")
            print_success(f"   ID: {usuario['id']}")
            print_success(f"   Email: {usuario['email']}")
            print_success(f"   Nombre: {usuario.get('full_name', 'N/A')}")
            print_success(f"   Rol: {usuario['role']}")
            return usuario
        else:
            print_error(f"Error obteniendo información: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print_error(f"Error obteniendo información: {e}")
        return None

def main():
    """Función principal - Pruebas de usuario"""
    print("🧪 PRUEBAS DE USUARIO NORMAL")
    print("🌐 URL:", BASE_URL)
    print("📧 Usuario: marcosflat@gmail.com")
    
    # 1. Login de usuario
    login_data = test_login_usuario()
    if not login_data:
        return False
    
    token = login_data["access_token"]
    
    # 2. Ver información del usuario
    test_ver_mi_informacion(token)
    
    # 3. Crear solicitud de certificado
    solicitud = test_crear_solicitud(token)
    if not solicitud:
        return False
    
    # 4. Ver todas las solicitudes del usuario
    test_ver_mis_solicitudes(token)
    
    print(f"\n{'🎉'*20}")
    print("🎉 ¡PRUEBAS DE USUARIO COMPLETADAS!")
    print("🎉 Usuario puede: Login, crear solicitud y ver sus solicitudes")
    print(f"{'🎉'*20}")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            print(f"\n{'⚠️'*20}")
            print("⚠️ Algunas pruebas de usuario fallaron")
            print(f"{'⚠️'*20}")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\n⏹️ Pruebas interrumpidas")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        sys.exit(1)