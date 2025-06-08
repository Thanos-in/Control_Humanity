import axios from 'axios'

const state = () => ({
  token: localStorage.getItem('token') || '',
  user: null,
})

const getters = {
  isAuthenticated: state => !!state.token,
  userRole: state => state.user ? state.user.role : null,
}

const actions = {
  async login({ commit }, credentials) {
    const response = await axios.post('/api/auth/login/', credentials)
    const token = response.data.access
    localStorage.setItem('token', token)
    axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
    commit('setToken', token)
    const userProfile = await axios.get('/api/auth/profile/')
    commit('setUser', userProfile.data)
  },
  logout({ commit }) {
    commit('logoutUser')
    localStorage.removeItem('token')
    delete axios.defaults.headers.common['Authorization']
  },
  async register({ dispatch }, userData) {
    await axios.post('/api/auth/register/', userData)
    await dispatch('login', {
      username: userData.username,
      password: userData.password,
    })
  },
}

const mutations = {
  setToken(state, token) {
    state.token = token
  },
  setUser(state, user) {
    state.user = user
  },
  logoutUser(state) {
    state.token = ''
    state.user = null
  },
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
