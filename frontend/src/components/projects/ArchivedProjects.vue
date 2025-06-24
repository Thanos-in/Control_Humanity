<template>
  <div class="relative overflow-x-auto shadow-md sm:rounded-lg">
    <table class="w-full text-sm text-left text-gray-500 dark:text-gray-400">
      <thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
        <tr>
          <th scope="col" class="px-6 py-3">Проекты</th>
          <th scope="col" class="px-6 py-3">Ответственный</th>
          <th scope="col" class="px-6 py-3">Период</th>
          <th scope="col" class="px-6 py-3">
            <span class="sr-only">Действия</span>
          </th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="proj in projects"
          :key="proj.id"
          class="bg-white border-b dark:bg-gray-800 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600"
        >
          <th
            scope="row"
            class="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white"
          >
            {{ proj.name }}
          </th>
          <td class="px-6 py-4">
            {{ proj.manager?.username || '—' }}
          </td>
          <td class="px-6 py-4">
            {{ proj.period }}
          </td>
          <td class="px-6 py-4 text-right">
            <a
              href="#"
              @click.prevent="goToProjectDetail(proj.id)"
              class="font-medium text-blue-600 dark:text-blue-500 hover:underline"
            >
              Изменить
            </a>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import api from "@/utils/axios";

export default {
  data() {
    return {
      openMenuId: null,
      projects: [],
    };
  },
  methods: {
    handleDocumentClick() {
      if (this.openMenuId) {
        this.openMenuId = null;
      }
    },
    toggleMenu(id) {
      this.openMenuId = this.openMenuId === id ? null : id;
    },
    goToTaskForm(taskId) {
      this.$router.push(`/taskform/${taskId}`);
    },
    goToProjectDetail(id) {
      this.$router.push(`/projects/${id}`);
    },
    async reloadArchivedProjects() {
      try {
        const { data } = await api.get("/projects/archivedprojects/");
        this.projects = data;
      } catch (e) {
        console.error("Проекты не загружены", e);
      }
    },
    async deleteProject(projectId) {
      try {
        await api.delete(`/projects/${projectId}/`);
        await this.reloadArchivedProjects(); 
      } catch (error) {
        console.error("O‘chirishda xatolik:", error);
      }
    },
  },
  async created() {
    await this.reloadArchivedProjects();
  },
  mounted() {
    document.addEventListener("click", this.handleDocumentClick);
  },
  beforeUnmount() {
    document.removeEventListener("click", this.handleDocumentClick);
  },
};
</script>
