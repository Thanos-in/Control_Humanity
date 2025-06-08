import axios from 'axios'

const state = () => ({
  ratings: [],
})

const getters = {
  allRatings: state => state.ratings,
}

const actions = {
  async fetchRatings({ commit }, received) {
    const response = await axios.get(`/api/ratings/?received=${received}`)
    commit('setRatings', response.data)
  },
  async rateUser({ dispatch }, ratingData) {
    await axios.post('/api/ratings/', ratingData)
    dispatch('fetchRatings', false)
  },
}

const mutations = {
  setRatings(state, ratings) {
    state.ratings = ratings
  },
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
