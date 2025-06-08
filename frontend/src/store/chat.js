import axios from 'axios'

const state = () => ({
  rooms: [],
  messages: [],
})

const getters = {
  allRooms: state => state.rooms,
  allMessages: state => state.messages,
}

const actions = {
  async fetchRooms({ commit }) {
    const response = await axios.get('/api/chat/rooms/')
    commit('setRooms', response.data)
  },
  async fetchMessages({ commit }, roomId) {
    const response = await axios.get(`/api/chat/messages/?chat_room=${roomId}`)
    commit('setMessages', response.data)
  },
  async sendMessage({ dispatch }, { roomId, content }) {
    await axios.post('/api/chat/messages/', { chat_room: roomId, content })
    dispatch('fetchMessages', roomId)
  },
}

const mutations = {
  setRooms(state, rooms) {
    state.rooms = rooms
  },
  setMessages(state, messages) {
    state.messages = messages
  },
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
