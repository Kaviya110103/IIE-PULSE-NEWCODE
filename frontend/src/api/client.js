import axios from 'axios'

const baseURL = import.meta.env.VITE_API_BASE_URL || "/api"
const api = axios.create({ baseURL })

// Logout after 5 minutes of no activity
const INACTIVITY_LIMIT = 5 * 60 * 1000
let inactivityTimer = null

export const resetInactivityTimer = () => {
  if (inactivityTimer) clearTimeout(inactivityTimer)

  inactivityTimer = setTimeout(() => {
    localStorage.clear()
    window.location.href = '/'
  }, INACTIVITY_LIMIT)
}

resetInactivityTimer()

;['mousedown', 'mousemove', 'keydown', 'scroll', 'touchstart', 'click'].forEach(event => {
  window.addEventListener(event, resetInactivityTimer, true)
})

api.interceptors.request.use(cfg => {
  resetInactivityTimer()

  const token = localStorage.getItem('access')
  if (token) cfg.headers.Authorization = `Bearer ${token}`

  return cfg
})

api.interceptors.response.use(
  r => r,
  async err => {
    const orig = err.config

    if (err.response?.status === 401 && !orig._retry) {
      orig._retry = true

      try {
        const refresh = localStorage.getItem('refresh')

        if (!refresh) {
          localStorage.clear()
          window.location.href = '/'
          return Promise.reject(err)
        }

        const { data } = await api.post('/auth/refresh/', { refresh })

        localStorage.setItem('access', data.access)
        orig.headers.Authorization = `Bearer ${data.access}`

        return api(orig)
      } catch {
        localStorage.clear()
        window.location.href = '/'
      }
    }

    return Promise.reject(err)
  }
)

export default api
