<template>
  <div class="">
    <h3 class="text-xl font-semibold mb-4 text-gray-200">Новый проект</h3>
    <form @submit.prevent="handleSubmit" class="bg-neutral-900/90 backdrop-blur-md border border-neutral-700 text-gray-200 p-6 rounded-lg shadow-lg w-full max-w-3xl">
      <div class="mb-4">
        <label class="block mb-1 font-medium" for="name">Название проекта</label>
        <input
          v-model="form.name"
          id="name"
          type="text"
          placeholder="Введите название проекта"
          class="w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-400 bg-neutral-800 text-gray-200"
        />
      </div>
      <div class="mb-4">
        <label class="block mb-1 font-medium" for="description">Описание</label>
        <textarea
          v-model="form.description"
          id="description"
          rows="3"
          placeholder="Введите описание проекта"
          class="w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-400 bg-neutral-800 text-gray-200"
        ></textarea>
      </div>
      <div class="mb-4">
        <label class="block mb-1 font-medium" for="manager_id">Назначить менеджера</label>
        <select
          v-model="form.manager_id"
          id="manager_id"
          class="w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-400 bg-neutral-800 text-gray-200"
        >
          <option disabled value="">Выберите менеджера</option>
          <option v-for="mgr in managers" :key="mgr.id" :value="mgr.id">
            {{ mgr.username }}
          </option>
        </select>
      </div>
      <div v-if="errorMessage" class="mb-4 text-red-400 text-sm">
        {{ errorMessage }}
      </div>
      <div class="flex justify-end space-x-2">
        <button
          type="button"
          @click="$emit('cancel')"
          class="px-4 py-2 border rounded hover:bg-gray-700 transition"
        >
          Отменить
        </button>
        <button
          type="submit"
          class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition"
          :disabled="loading"
        >
          <span v-if="loading">Добавление...</span>
          <span v-else>Добавить</span>
        </button>
      </div>
    </form>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'ProjectForm',
  data() {
    return {
      form: {
        name: '',
        description: '',
        manager_id: ''
      },
      managers: [],
      loading: false,
      errorMessage: ''
    }
  },
  methods: {
    async fetchManagers() {
      try {
        const response = await axios.get('/api/auth/users/managers/')
        // Agar backendda users/?role=manager endpoint bo‘lmasa, o‘zgartiring
        this.managers = response.data
      } catch (err) {
        console.error('Failed to fetch managers:', err)
      }
    },
    async handleSubmit() {
      this.errorMessage = ''
      if (!this.form.name) {
        this.errorMessage = 'Project name is required.'
        return
      }

      try {
        this.loading = true
        await this.$store.dispatch('projects/createProject', {
          name: this.form.name,
          description: this.form.description,
          manager_id: this.form.manager_id
        })
        this.$emit('saved')
      } catch (err) {
        this.errorMessage = 'Failed to create project.'
      } finally {
        this.loading = false
      }
    }
  },
  created() {
    this.fetchManagers()
  }
}
</script>
