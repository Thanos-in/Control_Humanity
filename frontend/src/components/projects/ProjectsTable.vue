<template>
  <div class="relative overflow-x-auto shadow-md sm:rounded-lg">
    <!-- Add Module and Task Modals -->
    <AddModuleModal
      v-if="showAddModuleModal"
      :project-id="selectedProjectForModule"
      @close="closeAddModuleModal"
      @saved="reloadProjects"
    />
    <AddTaskModal
      v-if="showAddTaskModal"
      :project-id="selectedProjectForTask.project"
      :module-id="selectedProjectForTask.module"
      @close="closeAddTaskModal"
      @saved="reloadProjects"
    />
    <table class="w-full text-sm text-left text-gray-500 dark:text-gray-400">
      <thead
        class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400"
      >
        <tr>
          <th class="px-6 py-3"></th>
          <th class="px-6 py-3">Проект / Модуль / Задача</th>
          <th class="px-6 py-3">Ответственный</th>
          <th class="px-6 py-3">Период</th>
          <th class="px-6 py-3">Статус</th>
          <th class="px-6 py-3">Выполнения</th>
          <th class="px-6 py-3">Действия</th>
          <!-- <th class="px-6 py-3 flex space-x-2 justify-end"></th> -->
        </tr>
      </thead>
      <tbody>
        <template v-for="proj in projects" :key="proj.id">
          <!-- Project Row -->
          <tr
            class="bg-white border-b dark:bg-gray-800 overflow-scroll dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600"
          >
            <td class="px-6 py-4">
              <button @click="toggleExpand(proj.id)" class="focus:outline-none">
                <svg
                  class="w-5 h-5 text-gray-500 dark:text-gray-400 transform transition-transform duration-200"
                  :class="{ 'rotate-180': expandedProjects.includes(proj.id) }"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M19 9l-7 7-7-7"
                  />
                </svg>
              </button>
            </td>
            <th
              scope="row"
              @click="selectProjectForChart(proj)"
              class="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white"
            >
              {{ proj.name }}
            </th>
            <td class="px-6 py-4">{{ proj.manager?.username || "—" }}</td>
            <td class="px-6 py-4">{{ proj.period }}</td>
            <td class="px-6 py-4">—</td>
            <td class="px-6 py-4">—</td>
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
                  Просмотр
                </li>
                <li
                  @click="openAddModuleModal(proj.id)"
                  class="px-4 py-2 hover:bg-gray-900 rounded-xl cursor-pointer text-left"
                >
                  Добавить модуль
                </li>
                <li
                  @click="openAddTaskModal(proj.id, null)"
                  class="px-4 py-2 hover:bg-gray-900 rounded-xl cursor-pointer text-left"
                >
                  Добавить задачу
                </li>
                <li
                  @click="editProject(proj.id)"
                  class="px-4 py-2 hover:bg-gray-900 rounded-xl cursor-pointer text-left"
                >
                  Изменить
                </li>
                <li
                  @click="confirmDelete('project', proj.id)"
                  class="px-4 py-2 hover:bg-gray-900 rounded-xl cursor-pointer text-left text-red-400 text-sm"
                >
                  Удалить
                </li>
              </ul>
            </td>
          </tr>

          <!-- Modules -->
          <template v-if="expandedProjects.includes(proj.id)">
            <template v-for="mod in proj.modules" :key="mod.id">
              <tr
                class="bg-white border-b dark:bg-gray-800 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600"
              >
                <td class="px-6 py-4"></td>
                <th
                  scope="row"
                  class="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white"
                >
                  <button
                    @click="toggleModule(mod.id)"
                    class="flex items-center space-x-2 focus:outline-none text-gray-900 dark:text-white"
                  >
                    <svg
                      class="w-5 h-5 transform transition-transform duration-200"
                      :class="{
                        'rotate-180': expandedModules.includes(mod.id),
                      }"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M19 9l-7 7-7-7"
                      />
                    </svg>
                    <span>{{ mod.name }}</span>
                  </button>
                </th>
                <td class="px-6 py-4"></td>
                <td class="px-6 py-4"></td>
                <td class="px-6 py-4"></td>
                <td class="px-6 py-4"></td>
                <td class="relative px-6 py-4 text-right">
                  <button
                    @click.stop="toggleMenu(`mod-${mod.id}`)"
                    class="focus:outline-none"
                  >
                    •••
                  </button>
                  <ul
                    v-if="openMenuId === `mod-${mod.id}`"
                    class="absolute right-0 mt-2 w-40 bg-gray-800 text-white rounded-xl border border-gray-700 rounded shadow-lg z-10"
                  >
                    <li
                      @click="openAddTaskModal(proj.id, mod.id)"
                      class="px-4 py-2 hover:bg-gray-900 rounded-xl cursor-pointer text-left"
                    >
                      Добавить задачу
                    </li>
                    <li
                      @click="editModule(mod.id)"
                      class="px-4 py-2 hover:bg-gray-900 rounded-xl cursor-pointer text-left"
                    >
                      Изменить
                    </li>
                    <li
                      @click="confirmDelete('module', mod.id)"
                      class="px-4 py-2 hover:bg-gray-900 rounded-xl cursor-pointer text-left text-red-400 text-sm"
                    >
                      Удалить
                    </li>
                  </ul>
                </td>
              </tr>
              <!-- Tasks -->
              <template v-if="expandedModules.includes(mod.id)">
                <tr
                  v-for="task in mod.tasks"
                  :key="task.id"
                  class="bg-white border-b dark:bg-gray-800 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600"
                >
                  <td class="px-6 py-4"></td>
                  <td class="px-6 py-4">📌 {{ task.title }}</td>
                  <td class="px-6 py-4">
                    {{ task.assigned_to?.username || "—" }}
                  </td>
                  <td class="px-6 py-4">
                    {{ formatPeriod(task.created_at, task.due_date) }}
                  </td>
                  <td class="px-6 py-4">
                    <span
                      :class="{
                        'text-green-600': task.status.name === 'done',
                        'text-yellow-600': task.status.name === 'in_progress',
                        'text-red-600': task.status.name === 'todo',
                      }"
                      >{{ statusLabel(task.status.name) }}</span
                    >
                  </td>
                  <td class="px-6 py-4">—</td>
                  <td class="relative px-6 py-4 text-right">
                    <button
                      @click.stop="toggleMenu(`task-${task.id}`)"
                      class="focus:outline-none"
                    >
                      •••
                    </button>
                    <ul
                      v-if="openMenuId === `task-${task.id}`"
                      class="absolute right-0 mt-2 w-40 bg-gray-800 text-white rounded-xl border border-gray-700 rounded shadow-lg z-10"
                    >
                      <li
                        @click="goToTaskForm(task.id)"
                        class="px-4 py-2 hover:bg-gray-900 rounded-xl cursor-pointer text-left"
                      >
                        Просмотреть
                      </li>
                      <li
                        @click="editTask(task.id)"
                        class="px-4 py-2 hover:bg-gray-900 rounded-xl cursor-pointer text-left"
                      >
                        Изменить
                      </li>
                      <li
                        @click="confirmDelete('task', task.id)"
                        class="px-4 py-2 hover:bg-gray-900 rounded-xl cursor-pointer text-left text-red-400 text-sm"
                      >
                        Удалить
                      </li>
                    </ul>
                  </td>
                </tr>
              </template>
            </template>
          </template>
        </template>
      </tbody>
    </table>
    <div class="fixed bottom-0 w-full z-50">
      <!-- <ProjectProgressChart
        class="mr-4"
        :project="selectedProjectForChart"
        :all-projects="projects"
      /> -->
    </div>
  </div>
</template>

<script>
import api from "@/utils/axios";
import AddModuleModal from "@/components/ui/AddModuleModal.vue";
import AddTaskModal from "@/components/ui/AddTaskModal.vue";
import ProjectProgressChart from "@/components/ui/ProjectProgressChart.vue";

export default {
  components: { AddModuleModal, AddTaskModal, ProjectProgressChart },
  data() {
    return {
      openMenuId: null,
      expandedProjects: [],
      expandedModules: [],
      projects: [],
      showAddModuleModal: false,
      showAddTaskModal: false,
      selectedProjectForChart: null,
      selectedProjectForModule: null,
      selectedProjectForTask: { project: null, module: null },
    };
  },
  async created() {
    await this.reloadProjects();
  },
  methods: {
    handleDocumentClick() {
      // agar ochiq menu bo‘lsa — yopamiz
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
    async reloadProjects() {
      try {
        const { data } = await api.get("/projects/");
        this.projects = data;
      } catch (e) {
        console.error("Проекты не загружены", e);
      }
    },
    toggleExpand(id) {
      const i = this.expandedProjects.indexOf(id);
      i === -1
        ? this.expandedProjects.push(id)
        : this.expandedProjects.splice(i, 1);
    },
    toggleModule(id) {
      const i = this.expandedModules.indexOf(id);
      i === -1
        ? this.expandedModules.push(id)
        : this.expandedModules.splice(i, 1);
    },
    openAddModuleModal(projectId) {
      this.selectedProjectForModule = projectId;
      this.showAddModuleModal = true;
    },
    selectProjectForChart(project) {
      this.selectedProjectForChart = project;
    },
    closeAddModuleModal() {
      this.showAddModuleModal = false;
      this.selectedProjectForModule = null;
    },
    openAddTaskModal(projectId, moduleId) {
      this.selectedProjectForTask = { project: projectId, module: moduleId };
      this.showAddTaskModal = true;
    },
    closeAddTaskModal() {
      this.showAddTaskModal = false;
      this.selectedProjectForTask = { project: null, module: null };
    },
    statusLabel(status) {
      const map = {
        done: "Завершен",
        in_progress: "В процессе",
        todo: "Не начат",
      };
      return map[status] || status;
    },
    formatPeriod(start, end) {
      const s = this.formatDate(start);
      const e = this.formatDate(end);
      return `${s} — ${e}`;
    },
    formatDate(dateStr) {
      if (!dateStr) return "?";
      return new Date(dateStr).toLocaleDateString("ru-RU");
    },
    getUnlinkedTasks(proj) {
      if (!proj.tasks) return [];
      return proj.tasks.filter(task => !task.module_id);
    },
  },
  mounted() {
    document.addEventListener("click", this.handleDocumentClick);
  },
  beforeUnmount() {
    document.removeEventListener("click", this.handleDocumentClick);
  },
};
</script>

<style scoped>
.rotate-180 {
  transform: rotate(180deg);
}
</style>
