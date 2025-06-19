<template>
  <div class="relative overflow-x-auto shadow-md sm:rounded-lg">
    <table
      class="w-full text-sm text-left rtl:text-right text-gray-500 dark:text-gray-400"
    >
      <thead
        class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400"
      >
        <tr>
          <th scope="col" class="px-6 py-3">Проекты</th>
          <th scope="col" class="px-6 py-3">Ответственный</th>
          <th scope="col" class="px-6 py-3">Период</th>
          <th scope="col" class="px-6 py-3">Действия</th>
        </tr>
      </thead>
      <tbody>
        <template v-for="proj in projects" :key="proj.id">
          <tr
            class="odd:bg-white odd:dark:bg-gray-900 even:bg-gray-50 even:dark:bg-gray-800 border-b dark:border-gray-700 border-gray-200"
          >
            <th
              scope="row"
              class="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white"
            >
              {{ proj.name }}
            </th>
            <td class="px-6 py-4">{{ proj.manager.username }}</td>
            <td class="px-6 py-4">{{ proj.period }}</td>
            <td class="relative px-6 py-4 text-right">
              <svg
                @click.stop="toggleMenu(`proj-${proj.id}`)"
                class="ml-auto w-4 h-4 text-gray-800 dark:text-white cursor-pointer"
                aria-hidden="true"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 20 20"
              >
                <path
                  stroke="currentColor"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M7.75 4H19M7.75 4a2.25 2.25 0 0 1-4.5 0m4.5 0a2.25 2.25 0 0 0-4.5 0M1 4h2.25m13.5 6H19m-2.25 0a2.25 2.25 0 0 1-4.5 0m4.5 0a2.25 2.25 0 0 0-4.5 0M1 10h11.25m-4.5 6H19M7.75 16a2.25 2.25 0 0 1-4.5 0m4.5 0a2.25 2.25 0 0 0-4.5 0M1 16h2.25"
                />
              </svg>
              <ul
                v-if="openMenuId === `proj-${proj.id}`"
                class="absolute right-0 mt-2 w-40 bg-gray-800 text-white border border-gray-700 rounded-xl shadow-lg z-10"
              >
                <li
                  @click="goToProjectDetail(proj.id)"
                  class="px-4 py-2 hover:bg-gray-900 rounded-xl cursor-pointer text-left"
                >
                  Изменить
                </li>
                <li
                  @click="deleteProject(proj.id)"
                  class="px-4 py-2 hover:bg-gray-900 rounded-xl cursor-pointer text-left text-red-400 text-sm"
                >
                  Удалить
                </li>
              </ul>
            </td>
          </tr>
        </template>
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
        await this.reloadArchivedProjects(); // o‘chirgandan keyin qayta yuklash
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
