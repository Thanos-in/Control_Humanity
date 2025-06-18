<template>
  <div class="grid grid-cols-[300px_1fr] h-full p-4 gap-6">
    <!-- Sidebar -->
    <aside class="bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-md">
      <img
        v-if="project.image"
        :src="project.image"
        alt="Project Image"
        class="w-full h-40 object-cover rounded-xl mb-6"
      />
      <h2 class="text-xl font-bold text-gray-900 dark:text-white mb-2">
        {{ project.name || "..." }}
      </h2>
    </aside>

    <!-- Main Content -->
    <section
      class="relative bg-white dark:bg-gray-800 p-8 rounded-2xl shadow-md"
    >
      <!-- Kanban Button -->
      <div class="absolute top-6 right-6 flex items-center space-x-2">
        <button
          type="button"
          class="text-white bg-gradient-to-r from-blue-500 via-blue-600 to-blue-700 hover:bg-gradient-to-br focus:ring-4 focus:outline-none focus:ring-blue-300 dark:focus:ring-blue-800 shadow-lg shadow-blue-500/50 dark:shadow-lg dark:shadow-blue-800/80 font-medium rounded-lg text-sm px-5 py-2.5 text-center"
        >
          Создать доску
        </button>
        <router-link
          :to="`/tasks/`"
          class="text-white bg-purple-600 hover:bg-purple-700 focus:ring-4 focus:ring-purple-300 dark:focus:ring-purple-800 font-medium rounded-lg text-sm px-5 py-2.5 shadow-md"
        >
          Kanban Board
        </router-link>
      </div>
      <div class="mb-6">
        <h3 class="text-lg font-semibold text-gray-800 dark:text-white mb-2">
          Описание
        </h3>
        <p class="text-gray-600 dark:text-gray-300 leading-relaxed">
          {{ project.description || "Описание недоступно." }}
        </p>
      </div>

      <div class="mt-6 space-y-4">
        <!-- Ответственный -->
        <div class="flex items-start gap-3">
          <span class="text-sm font-medium text-gray-800 dark:text-gray-200">
            Ответственный:
          </span>
          <p class="text-gray-800 dark:text-gray-200">
            {{ project.manager?.username || "Не указан" }}
          </p>
        </div>

        <!-- Период -->
        <div class="flex items-start gap-3">
          <span class="text-sm font-medium text-gray-800 dark:text-gray-200">
            Период:
          </span>
          <span class="w-9"></span>
          <p class="text-gray-800 dark:text-gray-200">
            {{ project.period || "Не указан" }}
          </p>
        </div>

    <!-- Архивирован checkbox bo'limi -->
    <div class="flex items-center gap-3 relative mt-4">
      <label
        :for="`archive-cbx-${project.id}`"
        class="text-sm font-medium text-gray-800 dark:text-gray-200"
      >
        Архивирован:
      </label>

      <!-- Checkbox input -->
      <input
        :id="`archive-cbx-${project.id}`"
        type="checkbox"
        :checked="project.is_archived"
        @change="toggleArchive"
        class="peer absolute w-6 h-6 ml-[115px] appearance-none border-2 border-gray-400 rounded-full transition-all duration-200 cursor-pointer hover:border-green-600 focus:outline-none"
      />

      <!-- Animatsion Label (splash) -->
      <label
        :for="`archive-cbx-${project.id}`"
        class="absolute w-6 h-6 bg-none ml-[115px] rounded-full pointer-events-none [filter:url(#goo)] peer-checked:animate-splash"
      ></label>

      <!-- Check icon -->
      <svg
        width="10"
        height="10"
        viewBox="0 0 15 14"
        fill="none"
        class="absolute top-[5px] ml-[115px] left-[7px] z-10 pointer-events-none"
      >
        <path
          d="M2 8.36364L6.23077 12L13 2"
          stroke="white"
          stroke-width="3"
          stroke-linecap="round"
          stroke-linejoin="round"
          class="stroke-dasharray-[19] stroke-dashoffset-[19] transition-all duration-500 peer-checked:stroke-dashoffset-0"
        />
      </svg>

      <!-- Gooey Filter (hidden) -->
      <svg xmlns="http://www.w3.org/2000/svg" version="1.1" class="hidden">
        <defs>
          <filter id="goo">
            <feGaussianBlur in="SourceGraphic" stdDeviation="4" result="blur" />
            <feColorMatrix
              in="blur"
              mode="matrix"
              values="1 0 0 0 0  
                      0 1 0 0 0  
                      0 0 1 0 0  
                      0 0 0 22 -7"
              result="goo"
            />
            <feBlend in="SourceGraphic" in2="goo" />
          </filter>
        </defs>
      </svg>
    </div>
            <!-- Status Table -->
        <div
          class="relative overflow-x-auto rounded-lg shadow scrollbar-black max-h-72 bg-white dark:bg-gray-900"
        >
          <template v-if="statuses && statuses.length">
            <!-- Status Table -->
            <div
              class="relative overflow-x-auto overflow-y-auto scrollbar-black shadow-md sm:rounded-lg"
            >
              <table
                class="w-full text-sm text-left text-gray-500 dark:text-gray-400"
              >
                <thead
                  class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400"
                >
                  <tr>
                    <th scope="col" class="p-4">
                      <div class="flex items-center">
                        <input
                          id="checkbox-all-status"
                          type="checkbox"
                          class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded-sm focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600"
                        />
                        <label for="checkbox-all-status" class="sr-only"
                          >Выбрать все</label
                        >
                      </div>
                    </th>
                    <th scope="col" class="px-6 py-3">Статус</th>
                    <th scope="col" class="px-6 py-3">Глобальный</th>
                    <th scope="col" class="px-6 py-3 text-right">
                      <button
                        @click="addStatus"
                        class="text-white bg-purple-600 hover:bg-purple-700 focus:ring-4 focus:ring-purple-300 dark:focus:ring-purple-800 font-medium rounded-lg text-sm px-5 py-2 shadow-md"
                      >
                        + Добавить статус
                      </button>
                    </th>
                  </tr>
                </thead>
                <tbody>
                  <tr
                    v-for="status in statuses"
                    :key="status.id"
                    class="bg-white border-b dark:bg-gray-800 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600"
                  >
                    <td class="w-4 p-4">
                      <div class="flex items-center">
                        <input
                          :id="`checkbox-status-${status.id}`"
                          type="checkbox"
                          class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded-sm focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600"
                        />
                        <label
                          :for="`checkbox-status-${status.id}`"
                          class="sr-only"
                          >Выбрать</label
                        >
                      </div>
                    </td>
                    <td
                      class="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white"
                    >
                      {{ status.name }}
                    </td>
                    <td class="px-6 py-4">
                      <span
                        class="inline-flex items-center justify-center w-5 h-5 rounded-full"
                        :class="
                          status.is_default ? 'bg-green-500' : 'bg-red-500'
                        "
                        title="По умолчанию"
                      >
                        <svg
                          v-if="status.is_default"
                          class="w-3 h-3 text-white"
                          fill="none"
                          stroke="currentColor"
                          stroke-width="2"
                          viewBox="0 0 24 24"
                        >
                          <path
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            d="M5 13l4 4L19 7"
                          />
                        </svg>
                        <svg
                          v-else
                          class="w-3 h-3 text-white"
                          fill="none"
                          stroke="currentColor"
                          stroke-width="2"
                          viewBox="0 0 24 24"
                        >
                          <path
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            d="M6 18L18 6M6 6l12 12"
                          />
                        </svg>
                      </span>
                    </td>
                    <td class="px-6 py-4 text-right" v-if="status.isNew">
                      <input
                        v-model="status.name"
                        placeholder="Название статуса"
                        class="border rounded px-2 py-1 mr-2"
                      />
                      <button
                        @click="saveNewStatus(status)"
                        class="px-2 py-1 bg-green-500 hover:bg-green-600 text-white rounded mr-1"
                      >
                        Сохранить
                      </button>
                      <button
                        @click="cancelNewStatus(status)"
                        class="px-2 py-1 bg-red-500 hover:bg-red-600 text-white rounded"
                      >
                        Отмена
                      </button>
                    </td>
                    <td class="px-6 py-4 text-right" v-else></td>
                  </tr>
                </tbody>
              </table>
            </div>
          </template>

          <template v-else>
            <div class="p-4 text-sm text-gray-600 dark:text-gray-300">
              Статусы отсутствуют.
            </div>
          </template>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import { mapActions } from "vuex";
import KanbanBoard from "../tasks/KanbanBoard.vue";
import api from "@/utils/axios"; // axios instance

export default {
  name: "ProjectDetail",
  components: { KanbanBoard },
  data() {
    return {
      project: {},
      statuses: [],
      error: null,
      loadingArchive: false, // ixtiyoriy: so‘rov davom etayotganini ko‘rsatish uchun
    };
  },
  computed: {
    projectId() {
      return parseInt(this.$route.params.id);
      return this.project?.id;
    },
  },
  methods: {
    ...mapActions("projects", ["fetchProjectById"]),
    async loadProject() {
      try {
        const response = await this.fetchProjectById(this.projectId);
        this.project = response;

        const statusResponse = await api.get(`/tasks/statuses/`);
        this.statuses = statusResponse.data;
      } catch (e) {
        this.error = "Failed to load project or statuses.";
        console.error(e);
      }
    },
    async toggleArchive(event) {
      const newArchived = event.target.checked;
      if (this.loadingArchive) return; 
      this.loadingArchive = true;
      try {
        const response = await api.patch(`/projects/${this.projectId}/archive/`, {
          is_archived: newArchived,
        });

        this.project = response.data;
      } catch (error) {
        console.error("Archive toggle error:", error);
        // event.target.checked = !newArchived;
        this.error = "Failed to update archive status.";
      } finally {
        this.loadingArchive = false;
      }
    },
  },
  created() {
    this.loadProject();
  },
};
</script>


<style scoped>
/* No additional styles needed; using Tailwind classes */
</style>
