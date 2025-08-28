import { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import Link from 'next/link';
import { certificadosAPI } from '../../../services/api';

export default function CertificadosEmitidos() {
  const [certificados, setCertificados] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const router = useRouter();

  useEffect(() => {
    cargarCertificados();
  }, []);

  const cargarCertificados = async () => {
    try {
      const token = localStorage.getItem('token');
      const todasSolicitudes = await certificadosAPI.misSolicitudes(token);
      
      // Filtrar solo los certificados emitidos
      const emitidos = todasSolicitudes.filter(s => s.status === 'Emitido');
      setCertificados(emitidos);
    } catch (error) {
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };

  const descargarCertificado = async (id, nombre) => {
    try {
      const token = localStorage.getItem('token');
      const blob = await certificadosAPI.descargarCertificado(token, id);
      
      // Crear link de descarga
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      
      // Determinar extensión del archivo
      const extension = blob.type === 'application/pdf' ? 'pdf' : 'txt';
      link.download = `certificado_${nombre}.${extension}`;
      
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
      
    } catch (error) {
      alert('Error al descargar el certificado: ' + error.message);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('userRole');
    localStorage.removeItem('userId');
    router.push('/login');
  };

  if (loading) return <div style={{ padding: '2rem', textAlign: 'center' }}>Cargando certificados...</div>;

  return (
    <div style={{ padding: '2rem', maxWidth: '1000px', margin: '0 auto' }}>
      {/* Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
        <h1>Mis Certificados Emitidos</h1>
        <div style={{ display: 'flex', gap: '1rem' }}>
          <Link href="/dashboard/usuario">
            <button style={{
              padding: '0.5rem 1rem',
              backgroundColor: '#6c757d',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer'
            }}>
              ← Volver
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

      {/* Lista de certificados */}
      <div>
        <h2 style={{ marginBottom: '1rem' }}>Certificados Disponibles ({certificados.length})</h2>
        
        {certificados.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '2rem', backgroundColor: '#f8f9fa', borderRadius: '4px' }}>
            <p>No tienes certificados emitidos aún</p>
            <p style={{ color: '#666', marginTop: '0.5rem' }}>
              Los certificados aparecerán aquí cuando un administrador apruebe tus solicitudes
            </p>
          </div>
        ) : (
          <div style={{ display: 'grid', gap: '1rem' }}>
            {certificados.map((certificado) => (
              <div key={certificado.id} style={{
                padding: '1.5rem',
                backgroundColor: 'white',
                border: '1px solid #ddd',
                borderRadius: '8px',
                boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center'
              }}>
                <div>
                  <h3 style={{ marginBottom: '0.5rem' }}>
                    {certificado.first_name} {certificado.last_name}
                  </h3>
                  <p><strong>Cédula:</strong> {certificado.identity_number}</p>
                  <p><strong>Fecha de emisión:</strong> {new Date(certificado.requested_at).toLocaleDateString()}</p>
                  <p><strong>UUID:</strong> {certificado.identity_number_uuid}</p>
                </div>
                
                <button
                  onClick={() => descargarCertificado(certificado.id, `${certificado.first_name}_${certificado.last_name}`)}
                  style={{
                    padding: '0.75rem 1.5rem',
                    backgroundColor: '#28a745',
                    color: 'white',
                    border: 'none',
                    borderRadius: '4px',
                    cursor: 'pointer',
                    fontSize: '1rem',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '0.5rem'
                  }}
                >
                  ⬇️ Descargar Certificado
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}