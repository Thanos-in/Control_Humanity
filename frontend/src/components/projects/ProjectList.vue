<template>
    <div class="max-w-4xl mx-auto">
      <div class="flex items-center justify-between mb-10">
        <h2 class="text-4xl font-bold text-white">Projects</h2>
        <button
          @click="showForm = true"
          class="bg-white text-purple-700 px-6 py-3 rounded-lg hover:bg-gray-100 shadow-md hover:shadow-lg transition font-semibold text-lg"
        >
          + New Project
        </button>
      </div>

      <!-- Xatolik bo'lsa chiqarilsin -->
      <div v-if="projectError" class="mb-6 text-red-100 bg-red-500 p-4 rounded-lg text-lg">
        {{ projectError }}
      </div>

      <!-- Loading paytida ko'rsatiladigan holat -->
      <div v-if="isLoading" class="text-center py-12">
        <span class="text-white opacity-90 text-xl">Loading projects...</span>
      </div>

      <!-- Project ro'yxati -->
      <ul v-else class="space-y-6">
        <li
          v-for="proj in projects"
          :key="proj.id"
          class="bg-white bg-opacity-90 p-6 rounded-2xl shadow-xl hover:shadow-2xl transition transform hover:scale-[1.01] min-h-[160px] flex flex-col justify-between"
        >
          <router-link :to="`/projects/${proj.id}`" class="block space-y-2">
            <h3 class="text-2xl font-semibold text-purple-800">{{ proj.name }}</h3>
            <p class="text-gray-700 text-base">{{ proj.description }}</p>
            <p class="mt-3 text-gray-600 text-sm">
              Director: {{ proj.director.username }}
              <span v-if="proj.manager"> | Manager: {{ proj.manager.username }}</span>
            </p>
          </router-link>
        </li>
      </ul>

      <!-- Modal: yangi loyiha qo'shish -->
      <Modal v-if="showForm" @close="showForm = false">
        <ProjectForm @saved="onProjectSaved" @cancel="showForm = false" />
      </Modal>
    </div>
  </template>

<script>
import { mapGetters, mapActions } from 'vuex'
import Modal from '../ui/Modal.vue'
import ProjectForm from './ProjectForm.vue'

export default {
  name: 'ProjectList',
  components: { Modal, ProjectForm },
  data() {
    return {
      showForm: false
    }
  },
  computed: {
    ...mapGetters('projects', ['allProjects', 'isLoading', 'projectError']),
    projects() {
      return this.allProjects
    }
  },
  methods: {
    ...mapActions('projects', ['fetchProjects']),
    onProjectSaved() {
      // Form ichida saqlangach, modalni yopamiz va ro'yxatni yangilaymiz
      this.showForm = false
      this.fetchProjects()
    }
  },
  created() {
    this.fetchProjects()
  }
}
</script>
