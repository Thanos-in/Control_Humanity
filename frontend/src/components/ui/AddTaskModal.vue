<template>
  <div v-if="visible" class="fixed inset-0 bg-black/50 z-50 flex items-center justify-center px-4">
    <div class="bg-white dark:bg-gray-800 p-6 rounded-xl w-full max-w-lg shadow-xl">
      <h2 class="text-lg font-semibold mb-4 text-gray-800 dark:text-white">
        Добавить задачу в
        <span class="text-blue-600">
          {{ module ? `модуль "${module.name}"` : `проект "${project.name}"` }}
        </span>
      </h2>

      <form @submit.prevent="submitTask">
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Название</label>
          <input v-model="form.title" required class="w-full p-2 rounded border dark:bg-gray-700 dark:text-white" />
        </div>

        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Описание</label>
          <textarea v-model="form.description" rows="3" class="w-full p-2 rounded border dark:bg-gray-700 dark:text-white"></textarea>
        </div>

        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Начало</label>
            <input v-model="form.start_date" type="date" class="w-full p-2 rounded border dark:bg-gray-700 dark:text-white" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Окончание</label>
            <input v-model="form.end_date" type="date" class="w-full p-2 rounded border dark:bg-gray-700 dark:text-white" />
          </div>
        </div>

        <div class="mt-4">
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Ответственный</label>
          <select v-model="form.assignee" class="w-full p-2 rounded border dark:bg-gray-700 dark:text-white">
            <option disabled value="">Выберите пользователя</option>
            <option v-for="user in users" :key="user.id" :value="user.id">
              {{ user.username }}
            </option>
          </select>
        </div>

        <div class="mt-6 flex justify-end gap-2">
          <button type="button" @click="$emit('close')" class="px-4 py-2 rounded bg-gray-300 hover:bg-gray-400 text-sm">
            Отмена
          </button>
          <button type="submit" class="px-4 py-2 rounded bg-blue-600 text-white hover:bg-blue-700 text-sm">
            Сохранить
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    visible: Boolean,
    project: Object,
    module: Object,
    users: Array,
  },
  data() {
    return {
      form: {
        title: '',
        description: '',
        start_date: '',
        end_date: '',
        assignee: '',
      },
    };
  },
  methods: {
    submitTask() {
      const payload = {
        ...this.form,
        project: this.project.id,
        module: this.module ? this.module.id : null,
      };
      this.$emit('submit', payload);
      this.resetForm();
    },
    resetForm() {
      this.form = {
        title: '',
        description: '',
        start_date: '',
        end_date: '',
        assignee: '',
      };
    },
  },
};
</script>
