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
        <div class="flex justify-between items-start">
          <router-link :to="`/projects/${proj.id}`" class="block space-y-2 flex-1 mr-4">
            <h3 class="text-2xl font-semibold text-purple-800">{{ proj.name }}</h3>
            <p class="text-gray-700 text-base">{{ proj.description }}</p>
            <p class="mt-3 text-gray-600 text-sm">
              Director: {{ proj.director.username }}
              <span v-if="proj.manager"> | Manager: {{ proj.manager.username }}</span>
            </p>
          </router-link>

          <!-- Delete button -->
          <button
            @click="confirmDelete(proj.id)"
            :disabled="deletingId === proj.id"
            class="text-red-600 hover:text-red-800 disabled:opacity-50"
            title="Delete Project"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
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
      showForm: false,
      deletingId: null // o'chirilayotgan project id
    }
  },
  computed: {
    ...mapGetters('projects', ['allProjects', 'isLoading', 'projectError']),
    projects() {
      return this.allProjects
    }
  },
  methods: {
    ...mapActions('projects', ['fetchProjects', 'deleteProject']),
    onProjectSaved() {
      // Form ichida saqlangach, modalni yopamiz va ro'yxatni yangilaymiz
      this.showForm = false
      this.fetchProjects()
    },
    async confirmDelete(projectId) {
      if (!confirm('Are you sure you want to delete this project?')) return
      this.deletingId = projectId
      try {
        await this.deleteProject(projectId)
      } catch (error) {
        console.error('Failed to delete project:', error)
      } finally {
        this.deletingId = null
        this.fetchProjects()
      }
    }
  },
  created() {
    this.fetchProjects()
  }
}
</script>
