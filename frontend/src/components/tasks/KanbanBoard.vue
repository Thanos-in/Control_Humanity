<template>
  <div class="flex gap-6 pb-6">
    <draggable
      :list="statuses"
      group="statuses"
      class="flex gap-6"
      @end="onStatusReorder"
      item-key="id"
      :animation="300"
    >
      <template #item="{ element: status }">
        <section
          class="w-80 rounded-xl p-4 shadow-md flex flex-col"
          :style="{ backgroundColor: status.color || '#ffffff' }"
          :data-status-id="status.id"
        >
          <!-- Header -->
          <header class="flex justify-between items-center mb-3">
            <h2
              class="text-base font-semibold truncate"
              :style="{ color: getTextColor(status.color) }"
            >
              {{ status.name }}
            </h2>

            <!-- "..." menyusi -->
            <div class="relative">
              <button
                @click="toggleDropdown(status.id)"
                class="text-gray-600 hover:text-gray-800 text-xl"
                title="Опции"
              >
                ...
              </button>

              <!-- Dropdown menyu tashqariga chiqadi -->
              <div
                v-if="activeDropdownId === status.id"
                class="absolute left-full top-0 ml-2 w-36 bg-white rounded-md shadow-lg z-50"
              >
                <button
                  @click="removeStatus(status.id)"
                  class="w-full flex items-center gap-2 px-4 py-2 text-sm font-medium text-red-700 bg-red-50 hover:bg-red-100 hover:text-red-800 transition-all rounded-md"
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    class="w-4 h-4"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M6 18L18 6M6 6l12 12"
                    />
                  </svg>
                  Удалить
                </button>
              </div>
            </div>
          </header>

          <!-- Tasklar -->
          <draggable
            :list="tasksByStatus(status.id)"
            group="tasks"
            @end="(evt) => onTaskReorder(evt, status.id)"
            class="flex-1 space-y-3 overflow-y-auto"
            item-key="id"
            :animation="250"
          >
            <template #item="{ element: task }">
              <div
                class="p-3 rounded-lg shadow-sm hover:shadow-md transition cursor-pointer"
                :style="{ backgroundColor: task.color || '#f0f0f0' }"
                @click.stop="openTaskForm(task)"
              >
                <TaskCard
                  :task="task"
                  @update-task="handleInlineUpdate"
                  class="cursor-move"
                  :text-color="getTextColor(task.color)"
                />

                <div
                  v-if="task.due_date"
                  class="mt-2 text-xs text-gray-200 bg-black bg-opacity-20 rounded-md px-2 py-1 inline-block"
                >
                  Срок: {{ formatDate(task.due_date) }}
                </div>
              </div>
            </template>
          </draggable>

          <!-- + Добавить карточку -->
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

    <!-- Add Status Column -->
    <section class="w-90 flex-shrink-0">
      <div
        v-if="!addingStatus"
        class="flex items-start justify-center mt-[10px]"
      >
        <button
          @click="startAddStatus"
          class="w-[280px] flex items-center justify-center px-4 py-2 bg-purple-700 bg-opacity-80 hover:bg-opacity-100 rounded-lg text-white text-sm font-medium cursor-pointer transition"
        >
          + Добавить статус
        </button>
      </div>

      <div v-else class="bg-black/90 p-4 rounded-xl w-80 space-y-3">
        <div class="flex items-center space-x-2">
          <input
            v-model="newStatusName"
            type="text"
            placeholder="Введите название статуса"
            class="flex-1 h-8 px-3 py-1 rounded border-none bg-gray-800 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-400"
          />
          <div class="flex items-center space-x-1">
            <span class="text-black"></span>
            <input
              type="color"
              v-model="newStatusColor"
              class="w-8 h-8 p-0 border-none bg-black rounded cursor-pointer"
              title="Выберите цвет"
            />
          </div>
        </div>

        <div class="flex justify-start space-x-3">
          <button
            @click="confirmAddStatus"
            class="h-8 px-4 py-0 bg-[#0000FF] text-black font-medium rounded-md shadow-md flex items-center justify-center"
            :disabled="statusLoading || !newStatusName.trim()"
          >
            <span v-if="statusLoading">Добавление...</span>
            <span v-else>Добавить список</span>
          </button>
          <button
            @click="cancelAddStatus"
            class="text-white text-xl hover:text-gray-300"
          >
            ✕
          </button>
        </div>
      </div>
    </section>
  </div>

  <!-- New Task Form Modal -->
  <div
    v-if="showTaskForm"
    class="fixed inset-0 bg-black bg-opacity-60 flex items-center justify-center z-50"
  >
    <div
      class="w-full max-w-lg p-8 rounded-xl shadow-2xl bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 text-white"
    >
      <h3 class="text-2xl font-bold mb-6">Создать новую задачу</h3>
      <form @submit.prevent="handleCreateTask" class="space-y-5">
        <!-- Task Title -->
        <div>
          <label class="block mb-1 font-medium text-white" for="title">
            Название задачи
          </label>
          <input
            v-model="newTask.title"
            id="title"
            type="text"
            placeholder="Введите название"
            class="w-full p-3 bg-white/10 border border-white/30 placeholder-white/60 text-white rounded-md focus:outline-none focus:ring-2 focus:ring-white focus:ring-opacity-50 text-base"
            required
          />
        </div>

        <!-- Description -->
        <div>
          <label class="block mb-1 font-medium text-white" for="description">
            Описание
          </label>
          <textarea
            v-model="newTask.description"
            id="description"
            rows="3"
            placeholder="Опишите задачу"
            class="w-full p-3 bg-white/10 border border-white/30 placeholder-white/60 text-white rounded-md focus:outline-none focus:ring-2 focus:ring-white focus:ring-opacity-50 text-base resize-none"
          ></textarea>
        </div>

        <!-- Assign To -->
        <div>
          <label class="block mb-1 font-medium text-white" for="assigned_to_id">
            Назначить
          </label>
          <select
            v-model="newTask.assigned_to_id"
            id="assigned_to_id"
            class="w-full p-3 bg-white/10 border border-white/30 text-black rounded-md focus:outline-none focus:ring-2 focus:ring-white focus:ring-opacity-50"
          >
            <option disabled value="">Выберите пользователя</option>
            <option v-for="mgr in users" :key="mgr.id" :value="mgr.id">
              {{ mgr.username }}
            </option>
          </select>
        </div>

        <!-- Due Date -->
        <div>
          <label class="block mb-1 font-medium text-white" for="due_date">
            Срок окончания
          </label>
          <input
            v-model="newTask.due_date"
            id="due_date"
            type="datetime-local"
            class="w-full p-3 bg-white/10 border border-white/30 placeholder-white/60 text-white rounded-md focus:outline-none focus:ring-2 focus:ring-white focus:ring-opacity-50 text-base"
          />
        </div>

        <!-- Color Picker -->
        <div class="flex items-center space-x-3">
          <label class="font-medium"> Цвет задачи: </label>
          <input
            type="color"
            v-model="newTask.color"
            class="w-8 h-8 rounded border border-black/30 p-0 appearance-none"
          />
        </div>

        <!-- Buttons -->
        <div class="flex justify-end space-x-4 mt-6">
          <button
            type="button"
            @click="showTaskForm = false"
            class="px-5 py-2 font-medium text-white/80 hover:text-white"
          >
            Отменить
          </button>
          <button
            type="submit"
            class="px-6 py-2 bg-white/20 text-white font-semibold rounded-md hover:bg-white/30 focus:outline-none focus:ring-2 focus:ring-white focus:ring-opacity-50"
          >
            Создать
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from "vuex";
import draggable from "vuedraggable";
import TaskCard from "./TaskCard.vue";
import axios from "axios";

export default {
  name: "KanbanBoard",
  components: { TaskCard, draggable },
  props: { projectId: { type: Number, required: true } },
  data() {
    return {
      showTaskForm: false,
      selectedTask: null,
      activeDropdownId: null,
      newTask: {
        title: "",
        description: "",
        status_id: null,
        color: "#f0f0f0",
        user_id: null,
        due_date: null,
      },
      users: [],
      addingStatus: false,
      newStatusName: "",
      user_id: null,
      newStatusColor: "#ffffff",
      statusLoading: false,
    };
  },
  computed: {
    ...mapState("tasks", ["tasks", "statuses"]),
    tasksByStatus() {
      return (statusId) =>
        this.tasks.filter(
          (task) =>
            (task.status.id || task.status) === statusId &&
            task.project.id === this.projectId
        );
    },
  },
  methods: {
    ...mapActions("tasks", [
      "fetchTasks",
      "fetchStatuses",
      "updateTask",
      "createTask",
      "createStatus",
      "updateStatus",
      "deleteStatus",
    ]),
    loadData() {
      this.fetchStatuses(this.projectId);
      this.fetchTasks(this.projectId);
    },
    toggleDropdown(statusId) {
      if (this.activeDropdownId === statusId) {
        this.activeDropdownId = null;
      } else {
        this.activeDropdownId = statusId;
      }
    },
    async fetchUsers() {
      try {
        const response = await axios.get("/api/auth/users/users/");
        this.users = response.data;
      } catch (err) {
        console.error("Failed to fetch users:", err);
      }
    },
    openTaskForm(task) {
      this.$router.push({ path: `/taskform/${task.id}` });
    },
    async onStatusReorder(evt) {
      const updates = this.statuses.map((s, idx) => ({ id: s.id, order: idx }));

      try {
        await Promise.all(
          updates.map((u) =>
            axios.patch(`/api/tasks/statuses/${u.id}/`, { order: u.order })
          )
        );

        this.statuses = [...this.statuses];

        // await this.fetchStatuses(this.projectId); // optional
      } catch (err) {
        console.error("Failed to reorder statuses:", err);
      }
    },
    async onTaskReorder(evt, oldStatusId) {
      const task = evt.item.__draggable_context.element;
      const newStatusId = Number(
        evt.to.closest("section[data-status-id]").dataset.statusId
      );
      if (oldStatusId === newStatusId) return;
      try {
        await axios.patch(`/api/tasks/${task.id}/`, { status_id: newStatusId });
        await this.fetchTasks(this.projectId);
      } catch (err) {
        console.error("Failed to update task:", err);
      }
    },
    async handleInlineUpdate(updatedTask) {
      await this.updateTask({
        taskId: updatedTask.id,
        payload: {
          status: newStatusId,
          title: updatedTask.title,
          description: updatedTask.description,
        },
      });
      this.fetchTasks(this.projectId);
    },
    startAddStatus() {
      this.addingStatus = true;
      this.newStatusName = "";
      this.newStatusColor = "#ffffff";
    },
    cancelAddStatus() {
      this.addingStatus = false;
      this.newStatusName = "";
      this.newStatusColor = "#ffffff";
    },
    async confirmAddStatus() {
      if (!this.newStatusName.trim()) return;
      this.statusLoading = true;
      await this.createStatus({
        name: this.newStatusName,
        color: this.newStatusColor,
        projectId: this.projectId,
        order: this.statuses.length + 1,
      });
      this.newStatusName = "";
      this.newStatusColor = "#ffffff";
      this.addingStatus = false;
      this.statusLoading = false;
      this.fetchStatuses(this.projectId);
    },
    async removeStatus(statusId) {
      await this.deleteStatus(statusId);
      this.fetchStatuses(this.projectId);
      this.fetchTasks(this.projectId);
    },
    openNewTaskForm(statusId) {
      this.newTask = {
        title: "",
        description: "",
        status_id: statusId,
        color: "#f0f0f0",
      };
      this.showTaskForm = true;
    },
    formatDate(dateString) {
      const options = {
        year: "numeric",
        month: "short",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
      };
      return new Date(dateString).toLocaleDateString(undefined, options);
    },
    async handleCreateTask() {
      await this.createTask({
        title: this.newTask.title,
        description: this.newTask.description,
        project_id: this.projectId,
        status_id: this.newTask.status_id,
        color: this.newTask.color || "#f0f0f0",
        assigned_to_id: this.newTask.assigned_to_id,
        user_id: this.newTask.user_id,
        due_date: this.newTask.due_date,
      });
      this.showTaskForm = false;
      this.fetchTasks(this.projectId);
    },
    getTextColor(bgColor) {
      if (!bgColor) return "#000000";
      const c = bgColor.substring(1);
      const rgb = parseInt(c, 16);
      const r = (rgb >> 16) & 0xff;
      const g = (rgb >> 8) & 0xff;
      const b = rgb & 0xff;
      const luminance = 0.299 * r + 0.587 * g + 0.114 * b;
      return luminance > 186 ? "#000000" : "#ffffff";
    },
  },
  created() {
    this.loadData();
    this.fetchUsers();
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
