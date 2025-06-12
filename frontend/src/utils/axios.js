// src/utils/axios.js
import axios from 'axios'
import store from '../store'
import router from '../router'

const instance = axios.create({
  baseURL: '/api', // optional
})

instance.interceptors.response.use(
  response => response,
  async error => {
    const originalRequest = error.config
    if (error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true
      const refresh = localStorage.getItem('refresh_token')
      if (refresh) {
        try {
          const res = await instance.post('/token/refresh/', { refresh })
          const newToken = res.data.access
          localStorage.setItem('token', newToken)
          instance.defaults.headers.common['Authorization'] = `Bearer ${newToken}`
          originalRequest.headers['Authorization'] = `Bearer ${newToken}`
          return instance(originalRequest)
        } catch {
          localStorage.clear()
          store.dispatch('auth/logout')
          router.push('/login')
        }
      }
    }
    return Promise.reject(error)
  }
)

export default instance

//interceptor 