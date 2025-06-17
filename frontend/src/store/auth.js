import api from '@/utils/axios' 
import router from '@/router'    

const state = () => ({
  token: localStorage.getItem('token') || '',
  refreshToken: localStorage.getItem('refresh_token') || '',
  user: null,
})

const getters = {
  isAuthenticated: state => !!state.token,
  userRole: state => state.user ? state.user.role : null,
  getUser: state => state.user,
}

const actions = {
  async checkAuth({ commit, state }) {
    if (state.token) {
      try {
        const res = await api.get('/auth/profile/')
        commit('setUser', res.data)
      } catch (err) {
        commit('logoutUser')
        localStorage.removeItem('token')
        localStorage.removeItem('refresh_token')
      }
    }
  },

  async login({ commit }, credentials) {
    try {
      const response = await api.post('/auth/login/', credentials)
      const access = response.data.access
      const refresh = response.data.refresh

      localStorage.setItem('token', access)
      localStorage.setItem('refresh_token', refresh)
      commit('setToken', access)
      commit('setRefreshToken', refresh)

      api.defaults.headers.common['Authorization'] = `Bearer ${access}`

      const profileRes = await api.get('/auth/profile/')
      commit('setUser', profileRes.data)

      return profileRes.data
    } catch (error) {
      throw error
    }
  },

  logout({ commit }) {
    commit('logoutUser')
    localStorage.removeItem('token')
    localStorage.removeItem('refresh_token')
    delete api.defaults.headers.common['Authorization']
    router.push({ path: '/' })
  },

  async register({ dispatch }, userData) {
    try {
      await api.post('/auth/register/', userData)
      await dispatch('login', {
        username: userData.username,
        password: userData.password,
      })
    } catch (error) {
      throw error
    }
  },
}

const mutations = {
  setToken(state, token) {
    state.token = token
  },
  setRefreshToken(state, refresh) {
    state.refreshToken = refresh
  },
  setUser(state, user) {
    state.user = user
  },
  logoutUser(state) {
    state.token = ''
    state.refreshToken = ''
    state.user = null
  },
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
}



//=============================================================>>>>


// import axios from 'axios'

// const state = () => ({
//   token: localStorage.getItem('token') || '',
//   user: null,
// })

// const getters = {
//   isAuthenticated: state => !!state.token,
//   userRole: state => state.user ? state.user.role : null,
// }

// const actions = {
//   async login({ commit }, credentials) {
//     const response = await axios.post('/api/auth/login/', credentials)
//     const token = response.data.access
//     localStorage.setItem('token', token)
//     axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
//     commit('setToken', token)
//     const userProfile = await axios.get('/api/auth/profile/')
//     commit('setUser', userProfile.data)
//   },
//   logout({ commit }) {
//     commit('logoutUser')
//     localStorage.removeItem('token')
//     delete axios.defaults.headers.common['Authorization']
//   },
//   async register({ dispatch }, userData) {
//     await axios.post('/api/auth/register/', userData)
//     await dispatch('login', {
//       username: userData.username,
//       password: userData.password,
//     })
//   },
// }

// const mutations = {
//   setToken(state, token) {
//     state.token = token
//   },
//   setUser(state, user) {
//     state.user = user
//   },
//   logoutUser(state) {
//     state.token = ''
//     state.user = null
//   },
// }

// export default {
//   namespaced: true,
//   state,
//   getters,
//   actions,
//   mutations
// }
