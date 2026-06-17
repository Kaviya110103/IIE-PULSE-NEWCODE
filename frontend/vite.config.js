import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

const parseAllowedHosts = () => {
  const hosts = process.env.VITE_ALLOWED_HOSTS
  return hosts ? hosts.split(',').map(host => host.trim()).filter(Boolean) : true
}

export default defineConfig({
  plugins: [react()],

  server: {
    host: '0.0.0.0',
    port: 5173,
    allowedHosts: parseAllowedHosts(),
  },

  preview: {
    host: '0.0.0.0',
    port: 8080,
    allowedHosts: parseAllowedHosts(),
  }
})
