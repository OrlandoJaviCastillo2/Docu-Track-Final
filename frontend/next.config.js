/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://localhost:8000/:path*', // Proxy a FastAPI
      },
    ];
  },
  // Configuración para evitar errores con React 19
  experimental: {
    esmExternals: true,
  },
};

module.exports = nextConfig;