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

def test_login_admin():
    """Prueba login de administrador"""
    print_step("1. LOGIN DE ADMINISTRADOR")
    
    login_data = {
        "email": "orlandojaviercastillo@gmail.com",
        "password": "orlan123"
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

def test_ver_todas_solicitudes(token):
    """Prueba ver todas las solicitudes"""
    print_step("2. VER TODAS LAS SOLICITUDES")
    
    auth_headers = {
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.get(
            f"{BASE_URL}/admin/solicitudes", 
            headers=auth_headers
        )
        
        if response.status_code == 200:
            solicitudes = response.json()
            print_success(f"Total de solicitudes en el sistema: {len(solicitudes)}")
            
            for i, solicitud in enumerate(solicitudes, 1):
                print_success(f"{i}. ID: {solicitud['id']}")
                print_success(f"   Solicitante: {solicitud['first_name']} {solicitud['last_name']}")
                print_success(f"   Cédula: {solicitud['identity_number']}")
                print_success(f"   Estado: {solicitud['status']}")
                print_success(f"   Fecha: {solicitud.get('requested_at', 'N/A')}")
                print("   " + "-"*40)
            
            return solicitudes
        else:
            print_error(f"Error obteniendo solicitudes: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print_error(f"Error obteniendo solicitudes: {e}")
        return None

def test_cambiar_estado_solicitud(token, solicitud_id, nuevo_estado):
    """Prueba cambiar estado de una solicitud"""
    print_step(f"3. CAMBIAR ESTADO A: {nuevo_estado}")
    
    auth_headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    update_data = {"status": nuevo_estado}
    
    try:
        response = requests.patch(
            f"{BASE_URL}/admin/solicitudes/{solicitud_id}", 
            json=update_data,
            headers=auth_headers
        )
        
        if response.status_code == 200:
            solicitud_actualizada = response.json()
            print_success(f"✅ Estado cambiado exitosamente!")
            print_success(f"   ID: {solicitud_actualizada['id']}")
            print_success(f"   Nuevo estado: {solicitud_actualizada['status']}")
            print_success(f"   Solicitante: {solicitud_actualizada['first_name']} {solicitud_actualizada['last_name']}")
            return solicitud_actualizada
        else:
            print_error(f"Error cambiando estado: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print_error(f"Error cambiando estado: {e}")
        return None

def test_ver_informacion_admin(token):
    """Prueba ver información del admin"""
    print_step("4. VER INFORMACIÓN DEL ADMINISTRADOR")
    
    auth_headers = {
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.get(
            f"{BASE_URL}/auth/me", 
            headers=auth_headers
        )
        
        if response.status_code == 200:
            admin = response.json()
            print_success("Información del administrador:")
            print_success(f"   ID: {admin['id']}")
            print_success(f"   Email: {admin['email']}")
            print_success(f"   Nombre: {admin.get('full_name', 'N/A')}")
            print_success(f"   Rol: {admin['role']}")
            return admin
        else:
            print_error(f"Error obteniendo información: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print_error(f"Error obteniendo información: {e}")
        return None

def main():
    """Función principal - Pruebas de administrador"""
    print("🧪 PRUEBAS DE ADMINISTRADOR")
    print("🌐 URL:", BASE_URL)
    print("📧 Admin: orlandojaviercastillo@gmail.com")
    
    # 1. Login de administrador
    login_data = test_login_admin()
    if not login_data:
        return False
    
    token = login_data["access_token"]
    
    # 2. Ver información del admin
    test_ver_informacion_admin(token)
    
    # 3. Ver todas las solicitudes
    solicitudes = test_ver_todas_solicitudes(token)
    if not solicitudes:
        return False
    
    # 4. Cambiar estado de la primera solicitud encontrada
    if solicitudes:
        primera_solicitud = solicitudes[0]
        print_step(f"ENCONTRADA SOLICitud PARA MODIFICAR: ID {primera_solicitud['id']}")
        
        # Cambiar a "En validación"
        test_cambiar_estado_solicitud(token, primera_solicitud['id'], "En validación")
        
        # Cambiar a "Emitido" (aprobado)
        test_cambiar_estado_solicitud(token, primera_solicitud['id'], "Emitido")
    else:
        print_success("⚠️ No hay solicitudes para modificar")
    
    print(f"\n{'🎉'*20}")
    print("🎉 ¡PRUEBAS DE ADMINISTRADOR COMPLETADAS!")
    print("🎉 Admin puede: Login, ver todas las solicitudes y cambiar estados")
    print(f"{'🎉'*20}")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            print(f"\n{'⚠️'*20}")
            print("⚠️ Algunas pruebas de administrador fallaron")
            print(f"{'⚠️'*20}")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\n⏹️ Pruebas interrumpidas")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        sys.exit(1)