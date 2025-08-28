// Formulario con: first_name, last_name, identity_number, birth_date
import { useState } from 'react';
import { useRouter } from 'next/router';
import Link from 'next/link';
import { certificadosAPI } from '../../../services/api';

export default function NuevaSolicitud() {
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    identity_number: '',
    birth_date: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const router = useRouter();

  const handleSubmit = async (e) => {
  e.preventDefault();
  setLoading(true);
  setError('');
  setSuccess('');

  try {
    const token = localStorage.getItem('token');
    // ✅ Ahora funciona con await directamente
    const data = await certificadosAPI.crearSolicitud(token, formData);
    
    setSuccess('Solicitud creada exitosamente!');
    setFormData({
      first_name: '',
      last_name: '',
      identity_number: '',
      birth_date: ''
    });
    
    setTimeout(() => {
      router.push('/dashboard/usuario');
    }, 2000);
  } catch (error) {
    setError(error.message);
  } finally {
    setLoading(false);
  }
};

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  return (
    <div style={{ padding: '2rem', maxWidth: '600px', margin: '0 auto' }}>
      {/* Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
        <h1>Nueva Solicitud de Certificado</h1>
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
      </div>

      {/* Formulario */}
      <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
        <div>
          <label>Nombre:</label>
          <input
            type="text"
            name="first_name"
            value={formData.first_name}
            onChange={handleChange}
            required
            style={{ width: '100%', padding: '0.75rem', border: '1px solid #ddd', borderRadius: '4px', fontSize: '1rem' }}
          />
        </div>

        <div>
          <label>Apellido:</label>
          <input
            type="text"
            name="last_name"
            value={formData.last_name}
            onChange={handleChange}
            required
            style={{ width: '100%', padding: '0.75rem', border: '1px solid #ddd', borderRadius: '4px', fontSize: '1rem' }}
          />
        </div>

        <div>
          <label>Número de Cédula:</label>
          <input
            type="text"
            name="identity_number"
            value={formData.identity_number}
            onChange={handleChange}
            required
            placeholder="Ej: 123-456789"
            style={{ width: '100%', padding: '0.75rem', border: '1px solid #ddd', borderRadius: '4px', fontSize: '1rem' }}
          />
        </div>

        <div>
          <label>Fecha de Nacimiento:</label>
          <input
            type="date"
            name="birth_date"
            value={formData.birth_date}
            onChange={handleChange}
            required
            style={{ width: '100%', padding: '0.75rem', border: '1px solid #ddd', borderRadius: '4px', fontSize: '1rem' }}
          />
        </div>

        {error && (
          <div style={{ color: 'red', padding: '1rem', backgroundColor: '#ffe6e6', border: '1px solid red' }}>
            {error}
          </div>
        )}

        {success && (
          <div style={{ color: '#155724', padding: '1rem', backgroundColor: '#d4edda', border: '1px solid #c3e6cb' }}>
            {success}
          </div>
        )}

        <button 
          type="submit" 
          disabled={loading}
          style={{
            padding: '1rem',
            backgroundColor: loading ? '#ccc' : '#0070f3',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: loading ? 'not-allowed' : 'pointer',
            fontSize: '1.1rem'
          }}
        >
          {loading ? 'Creando solicitud...' : 'Crear Solicitud'}
        </button>
      </form>
    </div>
  );
}