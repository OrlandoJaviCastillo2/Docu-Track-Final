import sys
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import psycopg2
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def test_connection():
    """Prueba la conexión directa a PostgreSQL con psycopg2"""
    print("🔍 Probando conexión directa a PostgreSQL...")
    try:
        conn = psycopg2.connect(
            dbname="docutrack_db",
            user="postgres",
            password=os.getenv("DB_PASSWORD", "admin123"),
            host="localhost",
            port="5432"
        )
        print("✅ Conexión directa EXITOSA con psycopg2")
        
        # Crear cursor y ejecutar consulta
        cur = conn.cursor()
        cur.execute("SELECT version();")
        db_version = cur.fetchone()
        print(f"📊 Versión de PostgreSQL: {db_version[0]}")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error en conexión directa: {e}")
        return False
    
    return True

def test_sqlalchemy_connection():
    """Prueba la conexión con SQLAlchemy"""
    print("\n🔍 Probando conexión con SQLAlchemy...")
    try:
        DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:admin123@localhost:5432/docutrack_db")
        engine = create_engine(DATABASE_URL)
        
        with engine.connect() as connection:
            result = connection.execute(text("SELECT version();"))
            version = result.scalar()
            print(f"✅ Conexión SQLAlchemy EXITOSA")
            print(f"📊 Versión: {version}")
            
        # Probar que puede acceder a las tablas
        with engine.connect() as connection:
            result = connection.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';"))
            tables = [row[0] for row in result]
            print(f"📋 Tablas en la base de datos: {tables}")
            
    except Exception as e:
        print(f"❌ Error en conexión SQLAlchemy: {e}")
        return False
    
    return True

def test_table_data():
    """Prueba que hay datos en las tablas"""
    print("\n🔍 Verificando datos en tablas...")
    try:
        DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:admin123@localhost:5432/docutrack_db")
        engine = create_engine(DATABASE_URL)
        
        with engine.connect() as connection:
            # Contar usuarios
            result = connection.execute(text("SELECT COUNT(*) FROM usuarios;"))
            user_count = result.scalar()
            print(f"👥 Usuarios en la base de datos: {user_count}")
            
            # Contar solicitudes
            result = connection.execute(text("SELECT COUNT(*) FROM solicitud_certificados;"))
            request_count = result.scalar()
            print(f"📋 Solicitudes en la base de datos: {request_count}")
            
            # Mostrar algunos usuarios
            if user_count > 0:
                result = connection.execute(text("SELECT id, email, full_name FROM usuarios LIMIT 5;"))
                print("📝 Usuarios encontrados:")
                for row in result:
                    print(f"   - ID: {row[0]}, Email: {row[1]}, Nombre: {row[2]}")
                    
    except Exception as e:
        print(f"❌ Error al leer datos: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("🧪 INICIANDO PRUEBAS DE CONEXIÓN A BASE DE DATOS")
    print("=" * 50)
    
    success1 = test_connection()
    success2 = test_sqlalchemy_connection() 
    success3 = test_table_data()
    
    print("\n" + "=" * 50)
    if success1 and success2 and success3:
        print("🎉 ¡TODAS LAS PRUEBAS EXITOSAS! La base de datos está conectada correctamente.")
    else:
        print("⚠️  Algunas pruebas fallaron. Revisa la configuración de la base de datos.")
    
    print("\n💡 Consejo: Si hay errores, verifica:")
    print("   - PostgreSQL está ejecutándose")
    print("   - La base de datos 'docutrack_db' existe")
    print("   - El usuario y contraseña son correctos")
    print("   - Las tablas fueron creadas correctamente")