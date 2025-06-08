import axios from 'axios'

const state = () => ({
  tasks: [],
  statuses: [],
  loadingTasks: false,
  loadingStatuses: false,
  error: null,
})

const getters = {
  allTasks: (state) => state.tasks,
  allStatuses: (state) => state.statuses,
  isLoadingTasks: (state) => state.loadingTasks,
  isLoadingStatuses: (state) => state.loadingStatuses,
  taskError: (state) => state.error,
}

const actions = {
  async fetchStatuses({ commit, rootState }, projectId) {
    commit('setLoadingStatuses', true)
    commit('setError', null)
    try {
      const token = rootState.auth.token
      const response = await axios.get(
        `/api/tasks/statuses/?project_id=${projectId}`,
        { headers: { Authorization: `Bearer ${token}` } }
      )
      const statusesData = Array.isArray(response.data) ? response.data : response.data.results
      commit('setStatuses', statusesData || [])
    } catch (err) {
      commit('setError', err)
    } finally {
      commit('setLoadingStatuses', false)
    }
  },

  async fetchTasks({ commit, rootState }, projectId) {
    commit('setLoadingTasks', true)
    commit('setError', null)
    try {
      const token = rootState.auth.token
      const response = await axios.get(
        `/api/tasks/?project_id=${projectId}`,
        { headers: { Authorization: `Bearer ${token}` } }
      )
      const tasksData = Array.isArray(response.data) ? response.data : response.data.results
      commit('setTasks', tasksData || [])
    } catch (err) {
      commit('setError', err)
    } finally {
      commit('setLoadingTasks', false)
    }
  },

  async updateTask({ commit }, { taskId, payload }) {
    commit('setError', null)
    try {
      const response = await axios.patch(
        `/api/tasks/${taskId}/`,
        payload,
      )
      commit('updateTaskInList', response.data)
    } catch (err) {
      commit('setError', err)
    }
  },

  async createTask({ commit }, taskData) {
    commit('setError', null)
    try {
      const response = await axios.post(
        '/api/tasks/',
        taskData,
      )
      commit('appendTask', response.data)
    } catch (err) {
      commit('setError', err)
    }
  },

  async createStatus({ commit }, statusData) {
    commit('setError', null)
    try {
      const response = await axios.post(
        '/api/tasks/statuses/',
        statusData,
      )
      commit('appendStatus', response.data)
    } catch (err) {
      commit('setError', err)
    }
  },

  async updateStatus({ commit }, { statusId, payload }) {
    commit('setError', null)
    try {
      const response = await axios.patch(
        `/api/tasks/statuses/${statusId}/`,
        payload,
      )
      commit('updateStatusInList', response.data)
    } catch (err) {
      commit('setError', err)
    }
  },

  async deleteStatus({ commit }, { statusId }) {
    commit('setError', null)
    try {
      await axios.delete(`/api/tasks/statuses/${statusId}/`)
      commit('removeStatus', statusId)
    } catch (err) {
      commit('setError', err)
    }
  },
}

const mutations = {
  setTasks(state, tasks) {
    state.tasks = tasks
  },
  setStatuses(state, statuses) {
    state.statuses = statuses.sort((a, b) => a.order - b.order)
  },
  appendTask(state, task) {
    state.tasks.push(task)
  },
  appendStatus(state, status) {
    state.statuses.push(status)
  },
  updateTaskInList(state, updatedTask) {
    const idx = state.tasks.findIndex((t) => t.id === updatedTask.id)
    if (idx !== -1) state.tasks.splice(idx, 1, updatedTask)
  },
  updateStatusInList(state, updatedStatus) {
    const idx = state.statuses.findIndex((s) => s.id === updatedStatus.id)
    if (idx !== -1) state.statuses.splice(idx, 1, updatedStatus)
    state.statuses.sort((a, b) => a.order - b.order)
  },
  removeStatus(state, statusId) {
    state.statuses = state.statuses.filter((s) => s.id !== statusId)
  },
  setLoadingTasks(state, isLoading) {
    state.loadingTasks = isLoading
  },
  setLoadingStatuses(state, isLoading) {
    state.loadingStatuses = isLoading
  },
  setError(state, error) {
    state.error = error
  },
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
}





// import axios from 'axios'

// const state = () => ({
//   tasks: [],
//   statuses: [],
// })

// const getters = {
//   allTasks: state => state.tasks,
//   allStatuses: state => state.statuses,
// }

// const actions = {
//   async fetchStatuses({ commit, rootState }, projectId) {
//     const token = rootState.auth.token
//     const response = await axios.get(`/api/tasks/statuses/?project_id=${projectId}`, {
//       headers: {
//         Authorization: `Bearer ${token}`
//       }
//     })
//     commit('setStatuses', response.data)
//   },
//   async fetchTasks({ commit, rootState }, projectId) {
//     const token = rootState.auth.token
//     const response = await axios.get(`/api/tasks/?project_id=${projectId}`, {
//       headers: {
//         Authorization: `Bearer ${token}`
//       }
//     })
//     commit('setTasks', response.data)
//   },
//   async updateTask({ rootState }, { taskId, payload }) {
//     const token = rootState.auth.token
//     await axios.patch(`/api/tasks/${taskId}/`, payload, {
//       headers: {
//         Authorization: `Bearer ${token}`
//       }
//     })
//   },
// }

// const mutations = {
//   setTasks(state, tasks) {
//     state.tasks = tasks
//   },
//   setStatuses(state, statuses) {
//     state.statuses = statuses
//   },
// }

// export default {
//   namespaced: true,
//   state,
//   getters,
//   actions,
//   mutations
// }






// import axios from 'axios'

// const state = () => ({
//   tasks: [],
//   statuses: [],
// })

// const getters = {
//   allTasks: state => state.tasks,
//   allStatuses: state => state.statuses,
// }

// const actions = {
//   async fetchStatuses({ commit }, projectId) {
//     const response = await axios.get(`/api/tasks/statuses/?project_id=${projectId}`)
//     commit('setStatuses', response.data)
//   },
//   async fetchTasks({ commit }, projectId) {
//     const response = await axios.get(`/api/tasks/?project_id=${projectId}`)
//     commit('setTasks', response.data)
//   },
//   async updateTask({ dispatch }, { taskId, payload }) {
//     await axios.patch(`/api/tasks/${taskId}/`, payload)
//   },
// }

// const mutations = {
//   setTasks(state, tasks) {
//     state.tasks = tasks
//   },
//   setStatuses(state, statuses) {
//     state.statuses = statuses
//   },
// }

// export default {
//   namespaced: true,
//   state,
//   getters,
//   actions,
//   mutations
// }
