import axios from 'axios'
import router from '@/router'    

const api = axios.create({
  baseURL: 'http://localhost:8000/api', 
})

let vuexStore = null

let isRefreshing = false
let failedQueue = []

const processQueue = (error, token = null) => {
  failedQueue.forEach(prom => {
    if (error) {
      prom.reject(error)
    } else {
      prom.resolve(token)
    }
  })
  failedQueue = []
}

//@param {Object} store - Vuex store instance

 export function setupInterceptors(store) {
  vuexStore = store

  api.interceptors.request.use(
    config => {
      const tokenFromState = vuexStore.state.auth.token
      const token = tokenFromState || localStorage.getItem('token')
      if (token) {
        config.headers.Authorization = `Bearer ${token}`
      }
      return config
    },
    error => Promise.reject(error)
  )

  api.interceptors.response.use(
    response => response,
    error => {
      const originalRequest = error.config
      if (
        error.response &&
        error.response.status === 401 &&
        !originalRequest._retry
      ) {
        if (isRefreshing) {
          return new Promise((resolve, reject) => {
            failedQueue.push({ resolve, reject })
          })
            .then(token => {
              originalRequest.headers.Authorization = `Bearer ${token}`
              return api(originalRequest)
            })
            .catch(err => Promise.reject(err))
        }

        originalRequest._retry = true
        isRefreshing = true

        const refreshFromState = vuexStore.state.auth.refreshToken
        const refresh = refreshFromState || localStorage.getItem('refresh_token')
        if (refresh) {
          return api
            .post('/token/refresh/', { refresh })
            .then(res => {
              const newToken = res.data.access
              localStorage.setItem('token', newToken)
              vuexStore.commit('auth/setToken', newToken)
              if (res.data.refresh) {
                const newRefresh = res.data.refresh
                localStorage.setItem('refresh_token', newRefresh)
                vuexStore.commit('auth/setRefreshToken', newRefresh)
              }
              api.defaults.headers.common['Authorization'] = `Bearer ${newToken}`
              processQueue(null, newToken)
              originalRequest.headers.Authorization = `Bearer ${newToken}`
              return api(originalRequest)
            })
            .catch(err => {
              processQueue(err, null)
              vuexStore.commit('auth/logoutUser')
              localStorage.removeItem('token')
              localStorage.removeItem('refresh_token')
              router.push({ name: '' })
              return Promise.reject(err)
            })
            .finally(() => {
              isRefreshing = false
            })
        } else {
          vuexStore.commit('auth/logoutUser')
          localStorage.removeItem('token')
          localStorage.removeItem('refresh_token')
          router.push({ name: 'Login' })
        }
      }
      return Promise.reject(error)
    }
  )
}

export default api
