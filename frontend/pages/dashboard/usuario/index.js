import { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import Link from 'next/link';
import { certificadosAPI } from '../../../services/api';

export default function DashboardUsuario() {
  const [solicitudes, setSolicitudes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const router = useRouter();

  useEffect(() => {
    cargarSolicitudes();
  }, []);

  const cargarSolicitudes = async () => {
  try {
    const token = localStorage.getItem('token');
    // Opera con await directamente
    const data = await certificadosAPI.misSolicitudes(token);
    setSolicitudes(data);
  } catch (error) {
    setError(error.message);
  } finally {
    setLoading(false);
  }
};

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('userRole');
    localStorage.removeItem('userId');
    router.push('/login');
  };

  if (loading) return <div style={{ padding: '2rem', textAlign: 'center' }}>Cargando...</div>;

  return (
    <div style={{ padding: '2rem', maxWidth: '1000px', margin: '0 auto' }}>
      {/* Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
        <h1>Panel de Usuario</h1>
        <button 
          onClick={handleLogout}
          style={{
            padding: '0.5rem 1rem',
            backgroundColor: '#dc3545',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer'
          }}
        >
          Cerrar Sesión
        </button>
      </div>

      {/* Botones de acción */}
      <div style={{ display: 'flex', gap: '1rem', marginBottom: '2rem' }}>
        <Link href="/dashboard/usuario/solicitar">
          <button style={{
            padding: '1rem 2rem',
            backgroundColor: '#0070f3',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer',
            fontSize: '1rem'
          }}>
            + Nueva Solicitud
          </button>
        </Link>

        <Link href="/dashboard/usuario/certificados">
          <button style={{
            padding: '1rem 2rem',
            backgroundColor: '#28a745',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer',
            fontSize: '1rem'
          }}>
            📄 Certificados Emitidos
          </button>
        </Link>
      </div>

      {/* Lista de solicitudes */}
      <div>
        <h2 style={{ marginBottom: '1rem' }}>Mis Solicitudes ({solicitudes.length})</h2>
        
        {error && (
          <div style={{ color: 'red', padding: '1rem', backgroundColor: '#ffe6e6', border: '1px solid red', marginBottom: '1rem' }}>
            {error}
          </div>
        )}

        {solicitudes.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '2rem', backgroundColor: '#f8f9fa', borderRadius: '4px' }}>
            <p>No tienes solicitudes aún</p>
            <Link href="/dashboard/usuario/solicitar">
              <button style={{
                padding: '0.5rem 1rem',
                backgroundColor: '#0070f3',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                cursor: 'pointer',
                marginTop: '1rem'
              }}>
                Crear primera solicitud
              </button>
            </Link>
          </div>
        ) : (
          <div style={{ display: 'grid', gap: '1rem' }}>
            {solicitudes.map((solicitud) => (
              <div key={solicitud.id} style={{
                padding: '1.5rem',
                backgroundColor: 'white',
                border: '1px solid #ddd',
                borderRadius: '8px',
                boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
              }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start' }}>
                  <div>
                    <h3 style={{ marginBottom: '0.5rem' }}>
                      {solicitud.first_name} {solicitud.last_name}
                    </h3>
                    <p><strong>Cédula:</strong> {solicitud.identity_number}</p>
                    <p><strong>Fecha nacimiento:</strong> {solicitud.birth_date}</p>
                    <p><strong>UUID:</strong> {solicitud.identity_number_uuid}</p>
                  </div>
                  
                  <div style={{ textAlign: 'right' }}>
                    <span style={{
                      padding: '0.25rem 0.75rem',
                      borderRadius: '12px',
                      fontSize: '0.875rem',
                      fontWeight: 'bold',
                      backgroundColor: 
                        solicitud.status === 'Emitido' ? '#d4edda' :
                        solicitud.status === 'En validación' ? '#fff3cd' :
                        solicitud.status === 'Rechazado' ? '#f8d7da' : '#e2e3e5',
                      color: 
                        solicitud.status === 'Emitido' ? '#155724' :
                        solicitud.status === 'En validación' ? '#856404' :
                        solicitud.status === 'Rechazado' ? '#721c24' : '#383d41'
                    }}>
                      {solicitud.status}
                    </span>
                    <p style={{ marginTop: '0.5rem', fontSize: '0.875rem', color: '#666' }}>
                      Solicitado: {new Date(solicitud.requested_at).toLocaleDateString()}
                    </p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}