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
    """Login de usuario"""
    print_step("1. LOGIN DE USUARIO")
    
    login_data = {
        "email": "marcosflat@gmail.com",
        "password": "muri1234"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            print_success("Login exitoso")
            return data
        else:
            print_error(f"Error en login: {response.status_code}")
            return None
            
    except Exception as e:
        print_error(f"Error de conexión: {e}")
        return None

def test_ver_certificados_emitidos(token):
    """Ver certificados emitidos"""
    print_step("2. VER CERTIFICADOS EMITIDOS")
    
    auth_headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{BASE_URL}/certificados/emitidos", headers=auth_headers)
        
        if response.status_code == 200:
            certificados = response.json()
            print_success(f"Certificados emitidos encontrados: {len(certificados)}")
            
            for cert in certificados:
                print_success(f"  - ID: {cert['id']}, Nombre: {cert['first_name']} {cert['last_name']}, Estado: {cert['status']}")
            
            return certificados
        else:
            print_error(f"Error obteniendo certificados: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print_error(f"Error obteniendo certificados: {e}")
        return None

def test_descargar_certificado(token, certificado_id):
    """Descargar un certificado"""
    print_step("3. DESCARGAR CERTIFICADO")
    
    auth_headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(
            f"{BASE_URL}/certificados/descargar/{certificado_id}", 
            headers=auth_headers,
            stream=True  # Para descargas grandes
        )
        
        if response.status_code == 200:
            # Guardar el PDF
            filename = f"certificado_{certificado_id}.pdf"
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print_success(f"✅ Certificado descargado: {filename}")
            print_success(f"   Tamaño: {len(response.content)} bytes")
            print_success(f"   Tipo: {response.headers.get('content-type')}")
            return True
        else:
            print_error(f"Error descargando certificado: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print_error(f"Error descargando certificado: {e}")
        return False

def main():
    """Pruebas de descarga de certificados"""
    print("🧪 PRUEBAS DE DESCARGA DE CERTIFICADOS")
    print("🌐 URL:", BASE_URL)
    
    # 1. Login
    login_data = test_login_usuario()
    if not login_data:
        return False
    
    token = login_data["access_token"]
    
    # 2. Ver certificados emitidos
    certificados = test_ver_certificados_emitidos(token)
    
    # 3. Descargar certificados (si hay alguno emitido)
    if certificados and len(certificados) > 0:
        for certificado in certificados:
            test_descargar_certificado(token, certificado["id"])
    else:
        print_success("⚠️ No hay certificados emitidos para descargar")
        print_success("💡 Un administrador debe cambiar el estado a 'Emitido' primero")
    
    print(f"\n{'🎉'*20}")
    print("🎉 Pruebas de certificados completadas!")
    print("💡 Recuerda que los certificados deben estar en estado 'Emitido'")
    print(f"{'🎉'*20}")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        print(f"\n{'⚠️'*20}")
        print("⚠️ Algunas pruebas fallaron")
        print(f"{'⚠️'*20}")
        sys.exit(1)