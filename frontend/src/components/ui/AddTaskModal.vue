<template>
  <div
    v-if="visible"
    class="fixed inset-0 flex items-center justify-center z-50 bg-neutral-900/90 backdrop-blur-md border border-neutral-700 text-gray-200"
  >
    <div
      class="w-full max-w-lg p-8 rounded-xl shadow-2xl bg-neutral-900/90 backdrop-blur-md border border-neutral-700 text-gray-200"
    >
      <h3 class="text-2xl font-bold mb-6">Создать новую задачу</h3>
      <!-- <form @submit.prevent="handleCreateTask" class="space-y-5"> -->
        <!-- Task Title -->
        <div>
          <label class="block mb-1 font-medium text-gray-200" for="title">
            Название задачи
          </label>
          <input
            v-model="newTask.title"
            id="title"
            type="text"
            placeholder="Введите название"
            class="w-full p-3 bg-white/10 border border-white/30 placeholder-white/60 text-gray-200 rounded-md focus:outline-none focus:ring-2 focus:ring-white focus:ring-opacity-50 text-base"
            required
          />
        </div>

        <!-- Description -->
        <div>
          <label class="block mb-1 font-medium text-gray-200" for="description">
            Описание
          </label>
          <textarea
            v-model="newTask.description"
            id="description"
            rows="3"
            placeholder="Опишите задачу"
            class="w-full p-3 bg-white/10 border border-white/30 placeholder-white/60 text-gray-200 rounded-md focus:outline-none focus:ring-2 focus:ring-white focus:ring-opacity-50 text-base resize-none"
          ></textarea>
        </div>

        <!-- Assign To -->
        <div>
          <label
            class="block mb-1 font-medium text-gray-200"
            for="assigned_to_id"
          >
            Назначить
          </label>
          <select
            v-model="newTask.assigned_to_id"
            id="assigned_to_id"
            class="w-full p-3 bg-white/10 border border-white/30 placeholder-white/60 text-gray-200 rounded-md focus:outline-none focus:ring-2 focus:ring-white focus:ring-opacity-50"
            required
          >
            <option disabled value="">Выберите пользователя</option>
            <option v-for="user in users" :key="user.id" :value="user.id">
              {{ user.username }}
            </option>
          </select>
        </div>

        <!-- Due Date -->
        <div>
          <label class="block mb-1 font-medium text-gray-200" for="due_date">
            Срок окончания
          </label>
          <input
            v-model="newTask.due_date"
            id="due_date"
            type="datetime-local"
            class="w-full p-3 bg-white/10 border border-white/30 placeholder-white/60 text-gray-200 rounded-md focus:outline-none focus:ring-2 focus:ring-white focus:ring-opacity-50 text-base"
          />
        </div>

        <!-- Color Picker -->
        <div class="flex items-center space-x-3">
          <label class="font-medium text-gray-200"> Цвет задачи: </label>
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
            @click="close"
            class="px-5 py-2 font-medium text-gray-200/80 hover:text-gray-200"
          >
            Отменить
          </button>
          <button
            @click="handleCreateTask"
            class="px-6 py-2 bg-gray-700/50 text-gray-200 font-semibold rounded-md hover:bg-gray-700/70 focus:outline-none focus:ring-2 focus:ring-gray-200 focus:ring-opacity-50"
          >
            Создать
          </button>
        </div>
      <!-- </form> -->
    </div>
  </div>
</template>

<script>

export default {
  name: "TaskFormModal",
  props: {
    visible: {
      type: Boolean,
      default: false,
    },
    projectId: {
      type: Number,
      required: true,
    },
    moduleId: {
      type: Number,
      default: null,
    },
    users: {
      type: Array,
      default: () => [],
    },
  },
  data() {
    return {
      newTask: {
        title: "",
        description: "",
        assigned_to_id: null,
        due_date: "",
        status_id: "39",
        color: "#FFFFFF",
      },
    };
  },
  methods: {
    close() {
      this.$emit("close");
      this.resetForm();
    },
    resetForm() {
      this.newTask = {
        title: "",
        description: "",
        assigned_to_id: null,
        status_id: "39",
        due_date: "",
        color: "#FFFFFF",
      };
    },
    async handleCreateTask() {
      const payload = {
        title: this.newTask.title,
        description: this.newTask.description,
        assigned_to_id: this.newTask.assigned_to_id,
        due_date: this.newTask.due_date
          ? new Date(this.newTask.due_date).toISOString()
          : null,
        color: this.newTask.color,
        project_id: this.projectId,
        status_id: "39",
        module_id: this.moduleId,
      };
      console.log("Yuborilayotgan payload:", payload);
      this.$emit("save", payload); 
      this.close();
    },
  },
};
</script>

<style scoped>
/* Add any specific styles here */
</style>
