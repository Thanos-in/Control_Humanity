<template>
  <div
    v-if="visible"
    class="fixed inset-0 bg-black bg-opacity-60 flex items-start justify-center pt-16 px-4 z-50"
  >
    <div
      class="bg-[#1e1f22] w-full max-w-6xl rounded-xl shadow-2xl max-h-[90vh] overflow-y-auto flex relative"
    >
      <!-- Form Panel -->
      <div class="w-2/3 p-6 space-y-6">
        <!-- Header -->
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-4xl font-bold text-gray-200">Создать новую задачу</h2>
          <button @click="close" class="text-gray-400 hover:text-gray-200">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-6 w-6"
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
          </button>
        </div>

        <!-- Title -->
        <div>
          <label for="title" class="block mb-1 font-medium text-gray-200"
            >Название задачи</label
          >
          <input
            id="title"
            v-model="newTask.title"
            type="text"
            placeholder="Введите название"
            class="w-full p-3 bg-[#2a2c2e] border border-gray-600 text-gray-200 rounded-md focus:outline-none focus:ring-2 focus:ring-gray-500"
            required
          />
        </div>
        
    <div class="flex justify-start items-start space-x-4">
      <!-- Участники (под заголовком) -->
      <div class="relative flex items-center space-x-2 mb-6">
        <span class="text-sm text-gray-400">Участники</span>
        <div class="flex items-center gap-2">
          <div
            v-for="id in newTask.marked_to_id"
            :key="id"
            class="w-8 h-8 rounded-full bg-green-600 text-white flex items-center justify-center text-xs"
            :title="getUserName(id)"
          >
            {{ initials(getUserName(id)) }}
          </div>
          <button
            @click.stop="showParticipants = !showParticipants; showLabels = false"
            ref="participantButton"
            class="w-8 h-8 rounded-full bg-white/10 border border-gray-600 flex items-center justify-center text-gray-200 hover:bg-white/20"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="w-5 h-5"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M12 4v16m8-8H4"
              />
            </svg>
          </button>
        </div>

        <!-- Participants Dropdown -->
        <div
          v-if="showParticipants"
          ref="participantDropdown"
          @click.stop
          class="absolute left-0 top-10 bg-[#1e1f22] border border-gray-600 rounded shadow-lg w-64 z-50"
        >
          <div class="p-2">
            <input
              v-model="participantSearch"
              type="text"
              placeholder="Поиск участников"
              class="w-full p-2 bg-[#2a2c2e] border border-gray-600 rounded text-sm text-gray-200 placeholder-gray-500 focus:outline-none"
            />
          </div>
          <div class="max-h-48 overflow-y-auto">
            <label
              v-for="u in filteredUsers"
              :key="u.id"
              class="flex items-center px-3 py-2 hover:bg-gray-700 cursor-pointer"
              @click="toggleParticipant(u.id)"
            >
              <div
                class="flex-shrink-0 w-6 h-6 mr-3 rounded-full bg-green-600 text-white flex items-center justify-center text-xs"
              >
                {{ initials(u.username) }}
              </div>
              <span class="flex-1 text-sm text-gray-200">{{ u.username }}</span>
              <span
                v-if="newTask.marked_to_id.includes(u.id)"
                class="text-gray-400"
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
                    d="M5 13l4 4L19 7"
                  />
                </svg>
              </span>
            </label>
          </div>
        </div>
      </div>

    <!-- Метки кнопка ва Dropdown -->
    <div class="relative mb-6">
      <button
        ref="labelButton"
        @click.stop="showLabels = !showLabels; showParticipants = false"
        class="px-3 py-1 flex items-center gap-2 bg-white/10 border border-gray-600 rounded-md text-gray-200 hover:bg-white/20"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="w-5 h-5"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M3 7h18M3 12h18M3 17h18"
          />
        </svg>
        Метка
      </button>

      <!-- Labels Dropdown -->
      <div
        v-if="showLabels"
        ref="labelDropdown"
        @click.stop
        class="absolute right-0 mt-2 w-48 bg-[#1e1f22] border border-gray-600 rounded shadow-lg z-50"
      >
        <div class="flex justify-between items-center px-4 py-2 border-b border-gray-700">
          <span class="text-gray-200 font-medium">Метки</span>
          <button
            @click="showLabels = false"
            class="text-gray-400 hover:text-gray-200"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="w-5 h-5"
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
          </button>
        </div>

        <div class="p-2">
          <input
            v-model="search"
            type="text"
            placeholder="Искать метки..."
            class="w-full p-2 bg-[#2a2c2e] border border-gray-600 rounded text-sm text-gray-200 placeholder-gray-500 focus:outline-none"
          />
        </div>

        <div class="max-h-40 overflow-y-auto">
          <label
            v-for="label in filteredLabels"
            :key="label.id"
            class="flex items-center px-4 py-2 hover:bg-gray-700 cursor-pointer"
            @click="selectLabel(label)"
          >
            <div
              :style="{ backgroundColor: label.color }"
              class="w-4 h-4 rounded mr-2 border border-gray-300"
            ></div>
            <div
              :style="{ backgroundColor: label.color }"
              class="flex-1 h-4 rounded"
            ></div>
          </label>
        </div>

        <div class="p-2 border-t border-gray-700">
          <button
            @click="createNewLabel"
            class="w-full px-3 py-2 bg-gray-700 text-gray-200 rounded hover:bg-gray-600"
          >
            Создать новую метку
          </button>
        </div>
      </div>
    </div>
  </div>

        <!-- Description -->
        <div>
          <label for="description" class="block mb-1 font-medium text-gray-200"
            >Описание</label
          >
          <textarea
            id="description"
            v-model="newTask.description"
            rows="3"
            placeholder="Опишите задачу"
            class="w-full p-3 bg-[#2a2c2e] border border-gray-600 text-gray-200 rounded-md focus:outline-none focus:ring-2 focus:ring-gray-500 resize-none"
          ></textarea>
        </div>

        <!-- Assign / Due / Color -->
        <div class="grid grid-cols-3 gap-6">
          <div>
            <label
              for="assigned_to_id"
              class="block mb-1 font-medium text-gray-200"
              >Назначить</label
            >
            <select
              id="assigned_to_id"
              v-model="newTask.assigned_to_id"
              class="w-full p-3 bg-[#2a2c2e] border border-gray-600 text-gray-200 rounded-md focus:outline-none focus:ring-2 focus:ring-gray-500"
              required
            >
              <option disabled value="">Выберите пользователя</option>
              <option v-for="u in users" :key="u.id" :value="u.id">
                {{ u.username }}
              </option>
            </select>
          </div>
          <div>
            <label for="due_date" class="block mb-1 font-medium text-gray-200"
              >Срок окончания</label
            >
            <input
              id="due_date"
              v-model="newTask.due_date"
              type="datetime-local"
              class="w-full p-3 bg-[#2a2f33] border border-gray-600 text-gray-200 rounded-md focus:outline-none focus:ring-2 focus:ring-gray-500"
            />
          </div>
          <!-- <div>
            <label class="block mb-1 font-medium text-gray-200">Метка</label>
            <input
              type="color"
              v-model="newTask.color"
              class="w-10 h-10 rounded-full border border-gray-600 p-0"
            />
          </div> -->
        </div>

        <!-- Actions -->
        <div class="flex justify-end space-x-4 mt-6">
          <button
            type="button"
            @click="close"
            class="px-6 py-2 text-sm font-medium text-gray-300 hover:text-gray-200"
          >
            Отменить
          </button>
          <button
            type="button"
            @click="handleCreateTask"
            class="px-6 py-2 bg-blue-600 text-black font-semibold rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            Создать
          </button>
        </div>
      </div>

      <!-- Side Panel (1/3) -->
      <div
        class="w-1/3 bg-[#242629] border-l border-gray-700 p-6 hidden md:flex flex-col"
      ></div>
    </div>
  </div>
</template>

<script>
export default {
  name: "TaskFormModal",
  props: {
    visible: Boolean,
    users: { type: Array, default: () => [] },
    projectId: Number,
    moduleId: { type: Number, default: null },
    labels: {
      type: Array,
      default: () => [
        { id: 1, color: "#2ecc71" },
        { id: 2, color: "#f1c40f" },
        { id: 3, color: "#e67e22" },
        { id: 4, color: "#e74c3c" },
        { id: 5, color: "#9b59b6" },
        { id: 6, color: "#3498db" },
      ],
    },
  },
  data() {
    return {
      newTask: {
        title: "",
        description: "",
        marked_to_id: [],
        assigned_to_id: null,
        due_date: "",
        status_id: 1,
        color: "#FFFFFF",
      },
      showParticipants: false,
      participantSearch: "",
      showLabels: false,
      search: "",
      selectedLabel: null,
    };
  },
  computed: {
    filteredUsers() {
      const s = this.participantSearch.toLowerCase();
      return this.users.filter((u) => u.username.toLowerCase().includes(s));
    },
    filteredLabels() {
      const s = this.search.toLowerCase();
      return this.labels.filter((l) => l.color.toLowerCase().includes(s));
    },
  },
  methods: {
    selectLabel(label) {
      this.showLabels = false;
      this.newTask.color = label.color;
      this.$emit("label-selected", label);
    },
    createNewLabel() {
      this.$emit("create-label");
    },
    handleClickOutside(event) {
      
    },
    handleClickOutside(e) {
      const participantDropdown = this.$refs.participantDropdown;
      const participantButton = this.$refs.participantButton;
      const labelDropdown = this.$refs.labelDropdown;
      const labelButton = this.$refs.labelButton;

      // Participants dropdown
      if (
        this.showParticipants &&
        participantDropdown &&
        participantButton &&
        !participantDropdown.contains(e.target) &&
        !participantButton.contains(e.target)
      ) {
        this.showParticipants = false;
      }

      // Labels dropdown
      if (
        this.showLabels &&
        labelDropdown &&
        labelButton &&
        !labelDropdown.contains(e.target) &&
        !labelButton.contains(e.target)
      ) {
        this.showLabels = false;
      }
    },
    initials(name) {
      return name
        .split(" ")
        .map((n) => n[0])
        .join("")
        .toUpperCase();
    },
    getUserName(id) {
      const u = this.users.find((x) => x.id === id);
      return u ? u.username : "";
    },
    toggleParticipant(id) {
      const idx = this.newTask.marked_to_id.indexOf(id);
      if (idx === -1) {
        this.newTask.marked_to_id.push(id);
        if (!this.newTask.assigned_to_id) this.newTask.assigned_to_id = id;
      } else {
        this.newTask.marked_to_id.splice(idx, 1);
        if (this.newTask.assigned_to_id === id) {
          this.newTask.assigned_to_id = this.newTask.marked_to_id[0] || null;
        }
      }
    },
    close() {
      this.$emit("close");
      this.resetForm();
    },
    resetForm() {
      this.newTask = {
        title: "",
        description: "",
        marked_to_id: [],
        assigned_to_id: null,
        due_date: "",
        status_id: 1,
        color: "#FFFFFF",
      };
      this.showParticipants = false;
      this.participantSearch = "";
    },
    handleCreateTask() {
      const payload = {
        ...this.newTask,
        due_date: this.newTask.due_date
          ? new Date(this.newTask.due_date).toISOString()
          : null,
        project_id: this.projectId,
        module_id: this.moduleId,
      };
      this.$emit("save", payload);
      this.close();
    },
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
/* Qo‘shimcha style kerak bo‘lsa shu yerga yozing */
</style>
