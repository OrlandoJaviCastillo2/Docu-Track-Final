import { useState } from 'react';
import { useRouter } from 'next/router';
import { authAPI } from '../services/api';

export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const router = useRouter();

const handleSubmit = async (e) => {
  e.preventDefault();
  setLoading(true);
  setError('');

  try {
    // ✅ Ahora funciona con await directamente
    const data = await authAPI.login(email, password);
    const { access_token, role, user_id } = data;

    localStorage.setItem('token', access_token);
    localStorage.setItem('userRole', role);
    localStorage.setItem('userId', user_id);

    if (role === 'administrador') {
      router.push('/dashboard/admin');
    } else {
      router.push('/dashboard/usuario');
    }
  } catch (error) {
    setError(error.message || 'Error en el login');
  } finally {
    setLoading(false);
  }
};

  return (
    <div style={{ padding: '2rem', maxWidth: '400px', margin: '0 auto' }}>
      <h1 style={{ textAlign: 'center', marginBottom: '2rem' }}>Iniciar Sesión</h1>
      
      <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
        <div>
          <label>Email:</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            style={{ width: '100%', padding: '0.5rem', marginTop: '0.25rem' }}
          />
        </div>
        
        <div>
          <label>Contraseña:</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            style={{ width: '100%', padding: '0.5rem', marginTop: '0.25rem' }}
          />
        </div>

        {error && (
          <div style={{ color: 'red', padding: '0.5rem', backgroundColor: '#ffe6e6', border: '1px solid red' }}>
            {error}
          </div>
        )}

        <button 
          type="submit" 
          disabled={loading}
          style={{
            padding: '0.75rem',
            backgroundColor: loading ? '#ccc' : '#0070f3',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: loading ? 'not-allowed' : 'pointer'
          }}
        >
          {loading ? 'Iniciando sesión...' : 'Iniciar Sesión'}
        </button>
      </form>

      <p style={{ textAlign: 'center', marginTop: '1rem' }}>
        ¿No tienes cuenta? <a href="/register" style={{ color: '#0070f3' }}>Regístrate aquí</a>
      </p>
    </div>
  );
}