const API_URL = 'http://localhost:8000';

// Función helper para manejar responses
const handleResponse = async (response) => {
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
  }
  return response.json();
};

export const authAPI = {
  login: async (email, password) => {
    const response = await fetch(`${API_URL}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });
    return handleResponse(response);
  },
  
  register: async (userData) => {
  const response = await fetch(`${API_URL}/auth/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(userData)
  });
  
  // Devuelve handleResponse(response) no response
  return handleResponse(response);
},

  getProfile: async (token) => {
    const response = await fetch(`${API_URL}/auth/me`, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    return handleResponse(response);
  }
};

export const certificadosAPI = {
  crearSolicitud: async (token, data) => {
    const response = await fetch(`${API_URL}/certificados/crear`, {
      method: 'POST',
      headers: { 
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify(data)
    });
    return handleResponse(response);
  },

  misSolicitudes: async (token) => {
    const response = await fetch(`${API_URL}/certificados/mis_solicitudes`, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    return handleResponse(response);
  },

  descargarCertificado: async (token, id) => {
    const response = await fetch(`${API_URL}/certificados/descargar/${id}`, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    
    if (!response.ok) {
      throw new Error('Error descargando certificado');
    }
    return response.blob();
  }
};

export const adminAPI = {
  todasSolicitudes: async (token) => {
    const response = await fetch(`${API_URL}/admin/solicitudes`, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    return handleResponse(response);
  },

  cambiarEstado: async (token, id, status) => {
    const response = await fetch(`${API_URL}/admin/solicitudes/${id}`, {
      method: 'PATCH',
      headers: { 
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({ status })
    });
    return handleResponse(response);
  }
};