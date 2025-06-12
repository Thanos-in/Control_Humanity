  import axios from 'axios'

  const state = () => ({
    rooms: [],
    messages: [],
    users: [],
  })

  const getters = {
    allRooms: state => state.rooms,
    allMessages: state => state.messages,
    allUsers: (state) => state.users,
  }

  const actions = {
    async fetchUsers({ commit }) {
      try {
        const response = await axios.get('/api/auth/users/allusers/') 
        commit('setUsers', response.data)
        return response.data
      } catch (error) {
        console.error('Error fetching users:', error)
        return []
      }
    },
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
    async deleteMessage({ commit }, { messageId }) {
      await axios.delete(`/api/chat/messages/${messageId}`)
      commit('removeMessage', messageId)
    },
    async createRoom({ dispatch }, participantIds) {
      try {
        const response = await axios.post('/api/chat/rooms/', {
          participant_ids: participantIds
        })

        await dispatch('fetchRooms')
        return response.data
      } catch (error) {
        console.error('Error creating room:', error)
        throw error
      }
  }
}


  const mutations = {
    setRooms(state, rooms) {
      state.rooms = rooms
    },
    setMessages(state, messages) {
      state.messages = messages
    },
    removeMessage(state, messageId) {
      state.messages = state.messages.filter(msg => msg.id !== messageId)
    },
    setUsers(state, users) {
      state.users = users
    }
  }

  export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
  }
