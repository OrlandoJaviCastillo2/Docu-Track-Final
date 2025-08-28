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

def test_health():
    """Prueba que el servidor esté funcionando"""
    print_step("1. VERIFICAR SALUD DEL SERVIDOR")
    try:
        response = requests.get(f"{BASE_URL}")
        if response.status_code == 200:
            print_success(f"Servidor funcionando: {response.json()}")
            return True
        else:
            print_error(f"Error: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print_error(f"No se pudo conectar al servidor: {e}")
        return False

def test_login(email, password, role_name):
    """Prueba login de usuario/administrador"""
    print_step(f"2. LOGIN DE {role_name.upper()}")
    print(f"📧 Email: {email}")
    print(f"🔑 Password: {password}")
    
    login_data = {"email": email, "password": password}
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data, headers=headers)
        
        print(f"📊 Código de respuesta: {response.status_code}")
        print(f"📊 Respuesta cruda: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            print_success(f"Login exitoso!")
            
            # Verificar diferentes formatos de respuesta
            if 'email' in data:
                print_success(f"   Email: {data['email']}")
            elif 'user_id' in data:
                print_success(f"   User ID: {data['user_id']}")
            
            if 'role' in data:
                print_success(f"   Rol: {data['role']}")
            
            if 'access_token' in data:
                print_success(f"   Token: {data['access_token'][:30]}...")
            else:
                print_error("   ❌ No se recibió access_token")
                
            return data
        else:
            print_error(f"Error en login: {response.status_code}")
            print_error(f"   Mensaje: {response.text}")
            return None
            
    except Exception as e:
        print_error(f"Error de conexión: {e}")
        return None

def test_user_info(token, expected_role):
    """Prueba obtener información del usuario"""
    print_step(f"3. INFORMACIÓN DE {expected_role.upper()}")
    
    auth_headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{BASE_URL}/auth/me", headers=auth_headers)
        
        if response.status_code == 200:
            user = response.json()
            print_success(f"Información obtenida:")
            print_success(f"   ID: {user['id']}")
            print_success(f"   Email: {user['email']}")
            print_success(f"   Rol: {user['role']}")
            return user
        else:
            print_error(f"Error: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print_error(f"Error: {e}")
        return None

def main():
    """Función principal"""
    print("🧪 PRUEBAS BÁSICAS DEL BACKEND")
    print("🌐 URL:", BASE_URL)
    print("💡 Probando solo salud del servidor y login")
    
    # Paso 1: Verificar servidor
    if not test_health():
        print("\n❌ El servidor no está funcionando. Ejecuta: python run.py")
        return False
    
    # Configuración - ¡EDITA ESTOS VALORES!
    print("\n📝 CONFIGURACIÓN:")
    print("   Usa los emails y contraseñas que USASTE al registrarte")
    
    # USUARIO NORMAL - Cambia estos valores
    USER_EMAIL = "marcosflat@gmail.com"    # 🔄 Cambia por tu email real
    USER_PASSWORD = "muri1234"              # 🔄 Cambia por tu password real
    
    # ADMINISTRADOR - Cambia estos valores  
    ADMIN_EMAIL = "orlandojaviercastillo@gmail.com"     # 🔄 Cambia por tu email real
    ADMIN_PASSWORD = "orlan123"        # 🔄 Cambia por tu password real
    
    # Paso 2: Login de usuario normal
    user_data = test_login(USER_EMAIL, USER_PASSWORD, "usuario")
    if not user_data:
        print("\n💡 Sugerencia: ¿Registraste este usuario? ¿La contraseña es correcta?")
        return False
    
    # Paso 3: Info del usuario
    test_user_info(user_data['access_token'], "usuario")
    
    # Paso 4: Login de administrador
    admin_data = test_login(ADMIN_EMAIL, ADMIN_PASSWORD, "administrador")
    if not admin_data:
        print("\n💡 Sugerencia: ¿Registraste este administrador? ¿La contraseña es correcta?")
        return False
    
    # Paso 5: Info del administrador
    test_user_info(admin_data['access_token'], "administrador")
    
    print(f"\n{'🎉'*20}")
    print("🎉 ¡PRUEBAS BÁSICAS COMPLETADAS!")
    print("🎉 El backend está funcionando correctamente")
    print(f"{'🎉'*20}")
    
    print(f"\n📋 RESUMEN:")
    print(f"   Servidor: ✅ Funcionando en {BASE_URL}")
    print(f"   Login usuario: ✅ {USER_EMAIL}")
    print(f"   Login admin: ✅ {ADMIN_EMAIL}")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            print(f"\n{'⚠️'*20}")
            print("⚠️  Algunas pruebas fallaron. Revisa los mensajes arriba.")
            print("💡 Asegúrate de:")
            print("   - El servidor esté ejecutándose (python run.py)")
            print("   - Usar emails y contraseñas REALES que hayas registrado")
            print("   - Los usuarios existan en la base de datos")
            print(f"{'⚠️'*20}")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\n⏹️  Pruebas interrumpidas por el usuario")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        sys.exit(1)