import api from '@/utils/axios'

const state = () => ({
  projects: [],
  loading: false,
  error: null
})

const getters = {
  allProjects: state => state.projects,
  isLoading: state => state.loading,
  projectError: state => state.error
}

const actions = {
  async fetchProjects({ commit }) {
    commit('setLoading', true)
    commit('setError', null)
    try {
      const response = await api.get('/projects/')
      commit('setProjects', response.data)
    } catch (err) {
      commit('setError', err.response?.data || 'Failed to fetch projects.')
    } finally {
      commit('setLoading', false)
    }
  },
  
  async fetchProjectById({ commit }, id) {
    const response = await api.get(`/projects/${id}/`);
    const project = response.data;
    commit("SET_PROJECT", project);
    return project; 
  },

  async createProject({ dispatch, commit }, projectData) {
    commit('setLoading', true)
    commit('setError', null)
    try {
      await api.post('/projects/', projectData)
      await dispatch('fetchProjects')
    } catch (err) {
      commit('setError', err.response?.data || 'Failed to create project.')
    } finally {
      commit('setLoading', false)
    }
  },

  async deleteProject({ commit }, projectId) {
    await api.delete(`/projects/${projectId}/`)
    commit('removeProject', projectId)
  }
}

const mutations = {
  setProjects(state, projects) {
    state.projects = projects
  },
  setLoading(state, loading) {
    state.loading = loading
  },
  setError(state, error) {
    state.error = error
  },
  removeProject(state, projectId) {
    state.projects = state.projects.filter(p => p.id !== projectId)
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}



//================================================================>>>>


// import axios from 'axios'

// const state = () => ({
//   projects: [],
//   loading: false,
//   error: null
// })

// const getters = {
//   allProjects: state => state.projects,
//   isLoading: state => state.loading,
//   projectError: state => state.error
// }

// const actions = {
//   async fetchProjects({ commit }) {
//     commit('setLoading', true)
//     commit('setError', null)
//     try {
//       const response = await axios.get('/api/projects/')
//       commit('setProjects', response.data)
//     } catch (err) {
//       commit('setError', err.response?.data || 'Failed to fetch projects.')
//     } finally {
//       commit('setLoading', false)
//     }
//   },
//   async createProject({ dispatch, commit }, projectData) {
//     commit('setLoading', true)
//     commit('setError', null)
//     try {
//       await axios.post('/api/projects/', projectData)
//       // Ro'yxatni yangilanadi!!!
//       await dispatch('fetchProjects')
//     } catch (err) {
//       commit('setError', err.response?.data || 'Failed to create project.')
//     } finally {
//       commit('setLoading', false)
//     }
//   },
//   async deleteProject({ commit }, projectId) {
//     await axios.delete(`/api/projects/${projectId}/`)
//     commit('removeProject', projectId)
//   }
// }

// const mutations = {
//   setProjects(state, projects) {
//     state.projects = projects
//   },
//   setLoading(state, loading) {
//     state.loading = loading
//   },
//   setError(state, error) {
//     state.error = error
//   },
//   removeProject(state, projectId) {
//     state.projects = state.projects.filter(p => p.id !== projectId)
//   }
// }

// export default {
//   namespaced: true,
//   state,
//   getters,
//   actions,
//   mutations
// }
