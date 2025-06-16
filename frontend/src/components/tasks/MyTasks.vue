<template>
  <!-- Основной контейнер канбан-доски -->
  <div class="flex gap-6 pb-6">
    <draggable
      :list="filteredStatuses"
      group="statuses"
      class="flex gap-6"
      @end="onStatusReorder"
      item-key="id"
      :animation="300"
    >
      <template #item="{ element: status }">
        <section
          class="mt-3 w-80 rounded-xl p-4 shadow-md flex flex-col"
          :style="{ backgroundColor: status.color || '#ffffff' }"
          :data-status-id="status.id"
        >
          <!-- Header -->
          <header class="flex justify-between items-center mb-3 relative">
            <div class="flex-1">
              <!-- Inline edit input or name -->
              <div
                v-if="inlineEditStatusId === status.id"
                class="flex items-center space-x-2"
              >
                <input
                  v-model="inlineEditStatusName"
                  type="text"
                  class="w-full px-2 py-1 rounded bg-gray-200 text-black"
                />
                <button
                  @click="confirmInlineEditStatus(status.id)"
                  class="text-green-600"
                >
                  ✔️
                </button>
                <button @click="cancelInlineEditStatus" class="text-red-600">
                  ✖️
                </button>
              </div>
              <h2
                v-else
                class="text-base font-semibold truncate"
                :style="{ color: getTextColor(status.color) }"
              >
                {{ status.name }}
              </h2>
            </div>
            <div class="flex items-center">
              <!-- Dropdown Trigger -->
              <div class="relative">
                <button
                  @click.stop="toggleDropdown(status.id)"
                  class="text-gray-600 hover:text-gray-800 text-xl"
                  title="Опции"
                >
                  ...
                </button>
                <!-- Dropdown Menu -->
                <div
                  v-if="activeDropdownId === status.id"
                  class="absolute right-0 top-full mt-2 w-36 bg-white rounded-md shadow-lg z-50 overflow-hidden"
                >
                  <button
                    @click="
                      startInlineEditStatus(status);
                      toggleDropdown(null);
                    "
                    class="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                  >
                    Изменить
                  </button>
                  <button
                    @click="
                      deleteStatus(status.id);
                      toggleDropdown(null);
                    "
                    class="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-gray-100"
                  >
                    Удалить
                  </button>
                </div>
              </div>
            </div>
          </header>

          <!-- Tasks -->
          <draggable
            :list="tasksByStatus(status.id)"
            group="tasks"
            @end="(evt) => onTaskReorder(evt, status.id)"
            class="flex-1 space-y-2 overflow-y-auto"
            item-key="id"
            :animation="200"
          >
            <template #item="{ element: task }">
              <div
                class="relative p-3 rounded-xl border border-neutral-700 bg-gradient-to-br from-neutral-800/90 to-neutral-900/90 backdrop-blur-md text-gray-100 flex flex-col cursor-pointer hover:border-gray-400 hover:shadow-md transition duration-200"
                :style="{ backgroundColor: task.color || '' }"
              >
                <!-- Header: title + dropdown -->
                <div class="flex items-center justify-between">
                  <h3
                    @click.stop="startEditTask(task)"
                    class="text-sm font-semibold truncate flex-1 pr-1"
                    :style="{ color: getTextColor(task.color) }"
                  >
                    {{ task.title }}
                  </h3>
                  <button
                    @click.stop="toggleTaskDropdown(task.id)"
                    class="text-gray-400 hover:text-white p-1"
                    title="Опции"
                  >
                    ⋮
                  </button>
                </div>

                <!-- Due Date (if exists) -->
                <div
                  v-if="task.due_date"
                  class="mt-2 text-[11px] text-gray-300 bg-white/10 backdrop-blur-sm rounded px-2 py-0.5 inline-block self-start"
                >
                  Срок: {{ formatDate(task.due_date) }}
                </div>

                <!-- Dropdown menu -->
                <div
                  v-if="activeTaskDropdownId === task.id"
                  class="fixed z-50 w-32 bg-neutral-900/95 backdrop-blur-md border border-neutral-700 rounded-lg shadow-xl overflow-hidden"
                >
                  <button
                    @click="
                      startEditTask(task);
                      toggleTaskDropdown(null);
                    "
                    class="w-full text-left text-[12px] px-3 py-2 hover:bg-neutral-800 transition"
                  >
                    Изменить
                  </button>
                  <button
                    @click="
                      deleteTask(task.id);
                      toggleTaskDropdown(null);
                    "
                    class="w-full text-left text-[12px] px-3 py-2 text-red-400 hover:bg-neutral-800 transition"
                  >
                    Удалить
                  </button>
                </div>
              </div>
            </template>
          </draggable>

          <!-- Add Card Button -->
          <button
            @click="openNewTaskForm(status.id)"
            class="mt-3 w-full flex items-center px-3 py-2 text-sm rounded-lg bg-transparent hover:shadow-sm hover:scale-[1.01] hover:backdrop-brightness-105 transition-all duration-200 ease-in-out cursor-pointer"
          >
            <div class="flex items-center space-x-2">
              <svg
                class="w-5 h-5 text-white"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M12 4v16m8-8H4"
                />
              </svg>
              <span class="text-white font-normal">Добавить карточку</span>
            </div>
          </button>
        </section>
      </template>
    </draggable>

    <!-- Column for Status Create/Edit -->
    <section class="w-90 flex-shrink-0">
      <div
        v-if="!addingStatus"
        class="flex items-start justify-center mt-[10px]"
      >
        <button
          @click="startAddStatus"
          class="w-[280px] flex items-center justify-center px-4 py-2 bg-purple-700 bg-opacity-80 hover:bg-opacity-100 rounded-lg text-white text-sm font-medium transition"
        >
          + Добавить статус
        </button>
      </div>
      <div
        v-else
        class="bg-neutral-900/90 border border-neutral-700 p-4 rounded-xl w-80 space-y-3 text-gray-200"
      >
        <div class="flex items-center space-x-2">
          <input
            v-model="newStatusName"
            type="text"
            placeholder="Введите название"
            class="flex-1 h-8 px-3 py-1 rounded bg-gray-800 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-400"
          />
          <input
            type="color"
            v-model="newStatusColor"
            class="w-8 h-8 p-0 border-none bg-black rounded cursor-pointer"
            title="Выберите цвет"
          />
        </div>
        <div class="flex space-x-3">
          <button
            @click="editingStatus ? confirmEditStatus() : confirmAddStatus()"
            class="h-8 px-4 bg-blue-600 text-white font-medium rounded shadow transition"
            :disabled="statusLoading || !newStatusName.trim()"
          >
            <span v-if="statusLoading">Сохранение...</span>
            <span v-else>{{ editingStatus ? "Сохранить" : "Добавить" }}</span>
          </button>
          <button @click="cancelAddStatus" class="text-white text-xl">✕</button>
        </div>
      </div>
    </section>
  </div>

  <!-- Task Modal -->
  <div
    v-if="showTaskForm"
    class="fixed inset-0 flex items-center justify-center z-50 bg-neutral-900/90 backdrop-blur-md"
  >
    <div class="w-full max-w-lg p-8 bg-neutral-800 rounded-xl shadow-2xl">
      <h3 class="text-2xl font-bold mb-4">
        {{ editingTask ? "Редактировать задачу" : "Новая задача" }}
      </h3>
      <form
        @submit.prevent="editingTask ? confirmEditTask() : handleCreateTask()"
        class="space-y-5"
      >
        <div>
          <label class="block mb-1 text-gray-200">Название</label>
          <input
            v-model="newTask.title"
            type="text"
            required
            class="w-full p-3 bg-gray-700 text-white rounded focus:ring-2 focus:ring-white"
          />
        </div>
        <div>
          <label class="block mb-1 text-gray-200">Описание</label>
          <textarea
            v-model="newTask.description"
            rows="3"
            class="w-full p-3 bg-gray-700 text-white rounded focus:ring-2 focus:ring-white"
          ></textarea>
        </div>
        <div>
          <label class="block mb-1 text-gray-200">Срок</label>
          <input
            v-model="newTask.due_date"
            type="datetime-local"
            class="w-full p-3 bg-gray-700 text-white rounded focus:ring-2 focus:ring-white"
          />
        </div>
        <div class="flex space-x-3 justify-end">
          <button
            type="submit"
            class="px-4 py-2 bg-green-600 rounded text-white transition"
          >
            Сохранить
          </button>
          <button
            @click="closeTaskForm"
            type="button"
            class="px-4 py-2 bg-red-600 rounded text-white transition"
          >
            Отмена
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { mapState } from "vuex";
import draggable from "vuedraggable";
import TaskCard from "./TaskCard.vue";

export default {
  name: "MyTasks",
  components: { TaskCard, draggable },
  data() {
    return {
      showTaskForm: false,
      addingStatus: false,
      editingStatus: null,
      editingTask: null,
      inlineEditStatusId: null,
      inlineEditStatusName: "",
      activeTaskDropdownId: null,
      newTask: {
        title: "",
        description: "",
        status: null,
        color: "#f0f0f0",
        due_date: null,
      },
      statuses: [],
      tasks: [],
      newStatusName: "",
      newStatusColor: "#ffffff",
      statusLoading: false,
      taskLoading: false,
      activeDropdownId: null,
    };
  },
  computed: {
    ...mapState("auth", ["user"]),
    filteredStatuses() {
      return this.statuses;
    },
    tasksByStatus() {
      return (statusId) => {
        return this.tasks.filter((task) => {
          const taskStatusId =
            task.status && typeof task.status === "object"
              ? task.status.id
              : task.status;

          let creatorId =
            task.created_by_id != null ? task.created_by_id : task.created_by;
          if (creatorId && typeof creatorId === "object") {
            creatorId = creatorId.id;
          }

          return taskStatusId === statusId && creatorId === this.user.id;
        });
      };
    },
  },
  methods: {
    toggleTaskDropdown(id) {
      this.activeTaskDropdownId = this.activeTaskDropdownId === id ? null : id;
    },
    toggleDropdown(statusId) {
      this.activeDropdownId =
        this.activeDropdownId === statusId ? null : statusId;
    },
    startInlineEditStatus(status) {
      this.inlineEditStatusId = status.id;
      this.inlineEditStatusName = status.name;
    },
    async confirmInlineEditStatus(id) {
      try {
        const res = await axios.patch(`/api/tasks/global-statuses/${id}/`, {
          name: this.inlineEditStatusName,
        });

        const idx = this.statuses.findIndex((s) => s.id === id);
        this.$set(this.statuses, idx, res.data);
      } catch (err) {
        console.error(err);
      }
      this.cancelInlineEditStatus();
    },
    cancelInlineEditStatus() {
      this.inlineEditStatusId = null;
      this.inlineEditStatusName = "";
    },
    async loadData() {
      try {
        const [statusRes, tasksRes] = await Promise.all([
          axios.get("/api/tasks/global-statuses/"),
          axios.get("/api/tasks/simple-tasks/"),
        ]);
        this.statuses = statusRes.data;
        this.tasks = tasksRes.data;
      } catch (err) {
        console.error("Load error:", err);
      }
    },
    startAddStatus() {
      this.addingStatus = true;
      this.editingStatus = null;
    },
    startEditStatus(status) {
      this.editingStatus = status;
      this.addingStatus = true;
      this.newStatusName = status.name;
      this.newStatusColor = status.color;
    },
    cancelAddStatus() {
      this.addingStatus = false;
      this.editingStatus = null;
      this.newStatusName = "";
      this.newStatusColor = "#ffffff";
    },
    async confirmAddStatus() {
      this.statusLoading = true;
      try {
        const res = await axios.post("/api/tasks/global-statuses/", {
          name: this.newStatusName,
          color: this.newStatusColor,
        });
        this.statuses.push(res.data);
      } catch (err) {
        console.error(err);
      } finally {
        this.statusLoading = false;
        this.cancelAddStatus();
      }
    },
    async confirmEditStatus() {
      this.statusLoading = true;
      try {
        const res = await axios.patch(
          `/api/tasks/global-statuses/${this.editingStatus.id}/`,
          { name: this.newStatusName, color: this.newStatusColor }
        );
        await this.loadData();
        const idx = this.statuses.findIndex(
          (s) => s.id === this.editingStatus.id
        );
        this.$set(this.statuses, idx, res.data);
      } catch (err) {
        console.error(err);
      } finally {
        this.statusLoading = false;
        this.cancelAddStatus();
      }
    },
    async deleteStatus(id) {
      if (!confirm("Удалить статус?")) return;
      try {
        await axios.delete(`/api/tasks/global-statuses/${id}/`);
        this.statuses = this.statuses.filter((s) => s.id !== id);
      } catch (err) {
        console.error(err);
      }
    },
    openNewTaskForm(statusId) {
      this.editingTask = null;
      this.newTask = {
        title: "",
        description: "",
        status: statusId, // status_id emas
        color: "#f0f0f0",
        due_date: null,
      };
      this.showTaskForm = true;
    },
    startEditTask(task) {
      this.editingTask = task;
      this.newTask = {
        title: task.title,
        description: task.description,
        status: task.status.id,
        color: task.color,
        due_date: task.due_date,
      };
      this.showTaskForm = true;
    },
    async confirmEditTask() {
      this.taskLoading = true;
      try {
        const payload = {
          title: this.newTask.title,
          description: this.newTask.description,
          status: this.newTask.status,
          color: this.newTask.color,
          due_date: this.newTask.due_date,
        };
        const res = await axios.patch(
          `/api/tasks/simple-tasks/${this.editingTask.id}/`,
          payload
        );
        await this.loadData();
        const idx = this.tasks.findIndex((t) => t.id === this.editingTask.id);
        this.$set(this.tasks, idx, res.data);
      } catch (err) {
        console.error(err);
      } finally {
        this.taskLoading = false;
        this.closeTaskForm();
      }
    },
    async handleCreateTask() {
      this.taskLoading = true;
      try {
        const payload = {
          title: this.newTask.title,
          description: this.newTask.description,
          status: this.newTask.status,
          color: this.newTask.color,
          due_date: this.newTask.due_date,
        };
        const res = await axios.post("/api/tasks/simple-tasks/", payload);
        this.tasks.push(res.data);
      } catch (err) {
        console.error(err);
      } finally {
        this.taskLoading = false;
        this.closeTaskForm();
      }
    },
    async deleteTask(id) {
      if (!confirm("Удалить задачу?")) return;
      try {
        await axios.delete(`/api/tasks/simple-tasks/${id}/`);
        await this.loadData();
        this.tasks = this.tasks.filter((t) => t.id !== id);
      } catch (err) {
        console.error(err);
      }
    },
    onStatusReorder(evt) {},
    onTaskReorder(evt, oldStatusId) {},
    closeTaskForm() {
      this.showTaskForm = false;
      this.editingTask = null;
    },
    formatDate(dateString) {
      const opts = {
        year: "numeric",
        month: "short",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
      };
      return new Date(dateString).toLocaleDateString(undefined, opts);
    },
    getTextColor(bgColor) {
      if (!bgColor) return "#000";
      const c = bgColor.substring(1);
      const rgb = parseInt(c, 16);
      const r = (rgb >> 16) & 0xff;
      const g = (rgb >> 8) & 0xff;
      const b = rgb & 0xff;
      const lum = 0.299 * r + 0.587 * g + 0.114 * b;
      return lum > 186 ? "#000" : "#fff";
    },
  },
  async created() {
    await this.loadData();
  },
  mounted() {
    document.addEventListener("click", this.handleClickOutside);
  },
  beforeUnmount() {
    document.removeEventListener("click", this.handleClickOutside);
  },
};
</script>

<style scoped>
.flex-1::-webkit-scrollbar {
  width: 6px;
}
.flex-1::-webkit-scrollbar-thumb {
  background-color: rgba(0, 0, 0, 0.2);
  border-radius: 3px;
}
</style>
