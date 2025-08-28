import { useState } from 'react';
import { useRouter } from 'next/router';
import Link from 'next/link';
import { authAPI } from '../services/api';

export default function Register() {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    full_name: '',
    role: 'usuario'
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState('');
  const router = useRouter();

  // Verificar si el usuario actual es admin para permitir registro de admins
  const isAdmin = typeof window !== 'undefined' && localStorage.getItem('userRole') === 'administrador';

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess('');

    try {
      // ✅ CORREGIDO: await directamente, sin response.json()
      const data = await authAPI.register(formData);
      
      setSuccess('Usuario registrado exitosamente!');
      setFormData({
        email: '',
        password: '',
        full_name: '',
        role: 'usuario'
      });

      // Si es admin, no redirigir a login
      if (!isAdmin) {
        setTimeout(() => {
          router.push('/login');
        }, 2000);
      }
    } catch (error) {
      setError(error.message || 'Error en el registro');
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
    <div style={{ padding: '2rem', maxWidth: '500px', margin: '0 auto' }}>
      {/* Botón de volver para admins */}
      {isAdmin && (
        <Link href="/dashboard/admin" style={{ display: 'block', marginBottom: '1rem' }}>
          <button style={{
            padding: '0.5rem 1rem',
            backgroundColor: '#6c757d',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer'
          }}>
            ← Volver al Dashboard
          </button>
        </Link>
      )}

      <h1 style={{ textAlign: 'center', marginBottom: '2rem' }}>
        {isAdmin ? 'Registrar Nuevo Usuario' : 'Crear Cuenta'}
      </h1>
      
      <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
        <div>
          <label>Nombre completo:</label>
          <input
            type="text"
            name="full_name"
            value={formData.full_name}
            onChange={handleChange}
            required
            style={{ width: '100%', padding: '0.75rem', border: '1px solid #ddd', borderRadius: '4px', fontSize: '1rem' }}
          />
        </div>

        <div>
          <label>Email:</label>
          <input
            type="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            required
            style={{ width: '100%', padding: '0.75rem', border: '1px solid #ddd', borderRadius: '4px', fontSize: '1rem' }}
          />
        </div>
        
        <div>
          <label>Contraseña (mínimo 6 caracteres):</label>
          <input
            type="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            required
            minLength="6"
            style={{ width: '100%', padding: '0.75rem', border: '1px solid #ddd', borderRadius: '4px', fontSize: '1rem' }}
          />
        </div>

        {/* Solo mostrar selector de rol para admins */}
        {isAdmin && (
          <div>
            <label>Tipo de usuario:</label>
            <select
              name="role"
              value={formData.role}
              onChange={handleChange}
              style={{ width: '100%', padding: '0.75rem', border: '1px solid #ddd', borderRadius: '4px', fontSize: '1rem' }}
            >
              <option value="usuario">Usuario Normal</option>
              <option value="administrador">Administrador</option>
            </select>
          </div>
        )}

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
          {loading ? 'Registrando...' : isAdmin ? 'Registrar Usuario' : 'Crear Cuenta'}
        </button>
      </form>

      {!isAdmin && (
        <p style={{ textAlign: 'center', marginTop: '1rem' }}>
          ¿Ya tienes cuenta? <a href="/login" style={{ color: '#0070f3' }}>Inicia sesión aquí</a>
        </p>
      )}
    </div>
  );
}