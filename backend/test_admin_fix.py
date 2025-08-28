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
    """Prueba login de administrador - CON DEBUG"""
    print_step("1. LOGIN DE ADMINISTRADOR (CON DEBUG)")
    
    login_data = {
        "email": "orlandojaviercastillo@gmail.com",
        "password": "orlan123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data, headers=headers)
        
        print(f"📊 Código de respuesta: {response.status_code}")
        print(f"📊 Respuesta completa: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            print_success("Login exitoso - ANALIZANDO TOKEN:")
            
            # Verificar todos los campos devueltos
            for key, value in data.items():
                if key == 'access_token':
                    print_success(f"{key}: {value[:50]}...")
                else:
                    print_success(f"{key}: {value}")
            
            return data
        else:
            print_error(f"Error en login: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print_error(f"Error de conexión: {e}")
        return None

def test_admin_access_with_token(token):
    """Probar acceso admin con token específico"""
    print_step("2. PROBAR ACCESO ADMIN CON TOKEN")
    
    auth_headers = {
        "Authorization": f"Bearer {token}"
    }
    
    try:
        # Probar endpoint de admin
        response = requests.get(
            f"{BASE_URL}/admin/solicitudes", 
            headers=auth_headers
        )
        
        print(f"📊 Código de respuesta: {response.status_code}")
        print(f"📊 Respuesta: {response.text}")
        
        if response.status_code == 200:
            print_success("✅ Acceso admin concedido!")
            return True
        else:
            print_error("❌ Acceso admin denegado")
            return False
            
    except Exception as e:
        print_error(f"Error de conexión: {e}")
        return False

def main():
    """Función principal para debug"""
    print("🐛 DEBUG DE ACCESO ADMINISTRADOR")
    print("🌐 URL:", BASE_URL)
    
    # 1. Login y ver qué devuelve
    login_data = test_login_admin()
    if not login_data:
        return False
    
    token = login_data["access_token"]
    
    # 2. Verificar el rol en el token
    print_step("3. VERIFICAR ROL EN EL TOKEN")
    print("💡 El token dice que el rol es:", login_data.get('role', 'NO ESPECIFICADO'))
    
    # 3. Probar acceso admin
    test_admin_access_with_token(token)
    
    print(f"\n{'🔍'*20}")
    print("🔍 ANÁLISIS COMPLETADO")
    print("💡 Si el rol en el token es 'usuario', el problema está en:")
    print("   - Cómo se genera el token durante el login")
    print("   - O cómo se guarda el rol en la base de datos")

if __name__ == "__main__":
    main()