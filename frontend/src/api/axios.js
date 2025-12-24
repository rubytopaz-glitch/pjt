import axios from 'axios'

const RAW_BASE = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api'
const BASE = RAW_BASE.replace(/\/$/, '') // 끝 / 제거

const api = axios.create({
  baseURL: BASE,
  withCredentials: false,
})

function getAccess() {
  return localStorage.getItem('access') || ''
}
function getRefresh() {
  return localStorage.getItem('refresh') || ''
}
function setTokens({ access, refresh }) {
  if (access) localStorage.setItem('access', access)
  if (refresh) localStorage.setItem('refresh', refresh)
}
function clearTokens() {
  localStorage.removeItem('access')
  localStorage.removeItem('refresh')
}

api.interceptors.request.use((config) => {
  const token = getAccess()
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

let isRefreshing = false
let queue = []

function flushQueue(error, token = null) {
  queue.forEach(({ resolve, reject }) => {
    if (error) reject(error)
    else resolve(token)
  })
  queue = []
}

api.interceptors.response.use(
  (res) => res,
  async (error) => {
    const original = error.config
    if (!original) return Promise.reject(error)

    // access 만료(401) -> refresh로 재발급
    if (error.response?.status === 401 && !original._retry) {
      original._retry = true

      const refresh = getRefresh()
      if (!refresh) {
        clearTokens()
        return Promise.reject(error)
      }

      if (isRefreshing) {
        return new Promise((resolve, reject) => {
          queue.push({
            resolve: (token) => {
              original.headers.Authorization = `Bearer ${token}`
              resolve(api(original))
            },
            reject,
          })
        })
      }

      isRefreshing = true
      try {
        // ✅ baseURL이 이미 /api 이므로, refresh는 /auth/refresh/ 만 붙이면 됨
        const r = await axios.post(`${BASE}/auth/refresh/`, { refresh })
        const newAccess = r.data.access
        setTokens({ access: newAccess })
        flushQueue(null, newAccess)

        original.headers.Authorization = `Bearer ${newAccess}`
        return api(original)
      } catch (e) {
        flushQueue(e, null)
        clearTokens()
        return Promise.reject(e)
      } finally {
        isRefreshing = false
      }
    }

    return Promise.reject(error)
  }
)

export default api
