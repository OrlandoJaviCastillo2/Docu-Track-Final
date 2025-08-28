import { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import Link from 'next/link';
import { adminAPI } from '../../../services/api';

export default function DashboardAdmin() {
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
      const data = await adminAPI.todasSolicitudes(token);
      setSolicitudes(data);
    } catch (error) {
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };

  const handleCambiarEstado = async (id, nuevoEstado) => {
    try {
      const token = localStorage.getItem('token');
      await adminAPI.cambiarEstado(token, id, nuevoEstado);
      
      // Recargar las solicitudes después de cambiar el estado
      await cargarSolicitudes();
      alert(`Estado cambiado a: ${nuevoEstado}`);
    } catch (error) {
      setError(error.message);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('userRole');
    localStorage.removeItem('userId');
    router.push('/login');
  };

  if (loading) return <div style={{ padding: '2rem', textAlign: 'center' }}>Cargando solicitudes...</div>;

  return (
    <div style={{ padding: '2rem', maxWidth: '1200px', margin: '0 auto' }}>
     {/* Header */}
<div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
  <h1>Panel de Administrador</h1>
  <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
    <Link href="/register">
      <button style={{
        padding: '0.5rem 1rem',
        backgroundColor: '#28a745',
        color: 'white',
        border: 'none',
        borderRadius: '4px',
        cursor: 'pointer'
      }}>
        + Registrar Usuario
      </button>
    </Link>
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
</div>

      {error && (
        <div style={{ color: 'red', padding: '1rem', backgroundColor: '#ffe6e6', border: '1px solid red', marginBottom: '1rem' }}>
          {error}
        </div>
      )}

      {/* Estadísticas rápidas */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '1rem', marginBottom: '2rem' }}>
        <div style={{ padding: '1rem', backgroundColor: '#e8f5e8', borderRadius: '8px', textAlign: 'center' }}>
          <h3>Total</h3>
          <p style={{ fontSize: '2rem', fontWeight: 'bold' }}>{solicitudes.length}</p>
        </div>
        <div style={{ padding: '1rem', backgroundColor: '#fff3cd', borderRadius: '8px', textAlign: 'center' }}>
          <h3>Pendientes</h3>
          <p style={{ fontSize: '2rem', fontWeight: 'bold' }}>
            {solicitudes.filter(s => s.status === 'Recibido').length}
          </p>
        </div>
        <div style={{ padding: '1rem', backgroundColor: '#d4edda', borderRadius: '8px', textAlign: 'center' }}>
          <h3>Emitidos</h3>
          <p style={{ fontSize: '2rem', fontWeight: 'bold' }}>
            {solicitudes.filter(s => s.status === 'Emitido').length}
          </p>
        </div>
        <div style={{ padding: '1rem', backgroundColor: '#f8d7da', borderRadius: '8px', textAlign: 'center' }}>
          <h3>Rechazados</h3>
          <p style={{ fontSize: '2rem', fontWeight: 'bold' }}>
            {solicitudes.filter(s => s.status === 'Rechazado').length}
          </p>
        </div>
      </div>

      {/* Lista de todas las solicitudes */}
      <div>
        <h2 style={{ marginBottom: '1rem' }}>Todas las Solicitudes ({solicitudes.length})</h2>

        {solicitudes.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '2rem', backgroundColor: '#f8f9fa', borderRadius: '4px' }}>
            <p>No hay solicitudes en el sistema</p>
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
                <div style={{ display: 'grid', gridTemplateColumns: '1fr auto', gap: '1rem', alignItems: 'start' }}>
                  {/* Información de la solicitud */}
                  <div>
                    <h3 style={{ marginBottom: '0.5rem' }}>
                      {solicitud.first_name} {solicitud.last_name}
                    </h3>
                    <p><strong>Cédula:</strong> {solicitud.identity_number}</p>
                    <p><strong>Fecha nacimiento:</strong> {solicitud.birth_date}</p>
                    <p><strong>UUID:</strong> {solicitud.identity_number_uuid}</p>
                    <p><strong>Solicitado:</strong> {new Date(solicitud.requested_at).toLocaleDateString()}</p>
                  </div>
                  
                  {/* Estado y acciones */}
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem', minWidth: '200px' }}>
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
                    </div>

                    {/* Acciones para cambiar estado */}
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                      <select
                        value={solicitud.status}
                        onChange={(e) => handleCambiarEstado(solicitud.id, e.target.value)}
                        style={{
                          padding: '0.5rem',
                          border: '1px solid #ddd',
                          borderRadius: '4px',
                          fontSize: '0.875rem'
                        }}
                      >
                        <option value="Recibido">Recibido</option>
                        <option value="En validación">En validación</option>
                        <option value="Rechazado">Rechazado</option>
                        <option value="Emitido">Emitido</option>
                      </select>

                      <button
                        onClick={() => handleCambiarEstado(solicitud.id, document.querySelector(`#estado-${solicitud.id}`).value)}
                        style={{
                          padding: '0.5rem',
                          backgroundColor: '#0070f3',
                          color: 'white',
                          border: 'none',
                          borderRadius: '4px',
                          cursor: 'pointer',
                          fontSize: '0.875rem'
                        }}
                      >
                        Actualizar Estado
                      </button>
                    </div>
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