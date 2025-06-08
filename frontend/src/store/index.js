import { createStore } from 'vuex'
import auth from './auth'
import projects from './projects'
import tasks from './tasks'
import chat from './chat'
import ratings from './ratings'

export default createStore({
  modules: {
    auth,
    projects,
    tasks,
    chat,
    ratings
  }
})
