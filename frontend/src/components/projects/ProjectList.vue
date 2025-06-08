<template>
  <div class="p-6 bg-gray-100 min-h-screen">
    <div class="max-w-3xl mx-auto">
      <div class="flex items-center justify-between mb-6">
        <h2 class="text-3xl font-semibold">Projects</h2>
        <button
          @click="showForm = true"
          class="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600 transition"
        >
          + New Project
        </button>
      </div>

      <!-- Xatolik bo'lsa chiqarilsin -->
      <div v-if="projectError" class="mb-4 text-red-600">
        {{ projectError }}
      </div>

      <!-- Loading paytida ko'rsatiladigan holat -->
      <div v-if="isLoading" class="text-center py-8">
        <span class="text-gray-500">Loading projects...</span>
      </div>

      <!-- Project ro'yxati -->
      <ul v-else class="space-y-4">
        <li
          v-for="proj in projects"
          :key="proj.id"
          class="bg-white p-4 rounded shadow hover:shadow-lg transition"
        >
          <router-link :to="`/projects/${proj.id}`" class="block">
            <h3 class="text-xl font-medium">{{ proj.name }}</h3>
            <p class="text-gray-600 text-sm">{{ proj.description }}</p>
            <p class="mt-2 text-gray-500 text-xs">
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
