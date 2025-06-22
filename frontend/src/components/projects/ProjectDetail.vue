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
          class="text-white bg-purple-600 hover:bg-purple-700 focus:ring-4 focus:ring-purple-300 dark:focus:ring-purple-800 font-medium rounded-lg text-sm px-5 py-2.5 shadow-md"
        >
          Kanban Board
        </router-link>
      </div>
      <div class="mb-6">
        <h3 class="text-lg font-semibold text-gray-800 dark:text-white mb-2">
          {{ $t("description") }}
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
            v-if="project.is_archived"
            :for="`archive-cbx-${project.id}`"
            class="text-sm font-medium text-gray-800 dark:text-gray-200"
          >
            Архивирован:
          </label>
          <label
            v-else
            :for="`archive-cbx-${project.id}`"
            class="text-sm font-medium text-gray-800 dark:text-gray-200"
          >
            Архивировать:
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
                <feGaussianBlur
                  in="SourceGraphic"
                  stdDeviation="4"
                  result="blur"
                />
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

        <!-- <div class="flex items-start gap-3">
          <span class="text-sm font-medium text-gray-800 dark:text-gray-200">
            Cвязанные задачи :
          </span>
          <p class="bottom-[535px] text-gray-800 dark:text-gray-200">
            {{ project.tasks.length }}
          </p>
        </div> -->
      </div>
    </section>
  </div>
  <div class="top-10">
    <KanbanBoard :projectId="projectId" />
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
      loadingArchive: false,
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
        const response = await api.patch(
          `/projects/${this.projectId}/archive/`,
          {
            is_archived: newArchived,
          }
        );

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
