import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import api, { setupInterceptors } from '@/utils/axios'
import './assets/tailwind.css'
import i18n from './i18n'

const app = createApp(App)
app.use(store)
app.use(router)
app.use(i18n)

// // v-click-outside direktiva
// app.directive('click-outside', {
//     beforeMount(el, binding) {
//       el.__clickOutsideHandler__ = event => {
//         // Agar click element ichida bo‘lmasa, funksiyani chaqir
//         if (!(el === event.target || el.contains(event.target))) {
//           binding.value(event)
//         }
//       }
//       document.addEventListener('click', el.__clickOutsideHandler__)
//     },
//     unmounted(el) {
//       document.removeEventListener('click', el.__clickOutsideHandler__)
//       el.__clickOutsideHandler__ = null
//     }
//   })

app.mount('#app')

setupInterceptors(store)

store.dispatch('auth/checkAuth')


//================================================================>>>>


// import { createApp } from 'vue'
// import App from './App.vue'
// import router from './router'
// import store from './store'
// import './assets/tailwind.css'
// import axios from 'axios'
// // import axios from '../utils/axios'

// const token = localStorage.getItem('token')
// if (token) {
//   axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
// }

// axios.interceptors.response.use(
//   response => response,
//   async error => {
//     const originalRequest = error.config

//     if (
//       error.response &&
//       error.response.status === 401 &&
//       !originalRequest._retry
//     ) {
//       originalRequest._retry = true
//       const refresh = localStorage.getItem('refresh_token')

//       if (refresh) {
//         try {
//           const res = await axios.post('/api/token/refresh/', {
//             refresh: refresh
//           })

//           const newAccessToken = res.data.access
//           localStorage.setItem('token', newAccessToken)
//           axios.defaults.headers.common['Authorization'] = `Bearer ${newAccessToken}`
//           originalRequest.headers['Authorization'] = `Bearer ${newAccessToken}`

//           return axios(originalRequest) // 🔁 So‘rovni qayta yuborish
//         } catch (refreshErr) {
//           // Refresh token ham eskirgan bo‘lsa — logout
//           localStorage.removeItem('token')
//           localStorage.removeItem('refresh_token')
//           store.dispatch('auth/logout')
//           router.push('/login')
//         }
//       }
//     }

//     return Promise.reject(error)
//   }
// )

// const app = createApp(App)
// app.use(store)
// app.use(router)
// app.mount('#app')
