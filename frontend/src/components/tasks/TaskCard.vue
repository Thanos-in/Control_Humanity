<template>
  <div class="h-25 bg-neutral-900/90 backdrop-blur-md rounded-lg text-gray-200 p-4 rounded shadow">
    <div class="flex items-center mb-2">
      <input
        id="checkbox-{{ task.id }}"
        type="checkbox"
        v-model="localCompleted"
        @change="$emit('update-task', { ...task, completed: localCompleted })"
        class="mt-0 w-4 h-4 text-green-600 bg-green-100 border-green-300 rounded-full focus:ring-green-500 focus:ring-2"
      />
      <label
        :for="'checkbox-' + task.id"
        class="ms-2 text-sm font-medium text-green-900 dark:text-green-300"
      >
        <!-- Bu label bo‘sh qolsa ham, click input-ga tegadi -->
      </label>
      <h4 class="font-medium ml-1 truncate" :title="task.title">{{ task.title }}</h4>
    </div>

    <!--
    <p class="text-sm text-gray-600 mb-2">
      {{
        task.description && task.description.length > 50
          ? task.description.slice(0, 50) + "…"
          : task.description
      }}
    </p>
    -->

    <div
      v-if="task.due_date"
      class="mt-2 text-xs text-gray-700 bg-gray-100 rounded-md px-2 py-1 inline-block"
      :title="formatDate(task.due_date)"
    >
      <svg xmlns="http://www.w3.org/2000/svg" class="inline w-3 h-3 mr-1 align-text-bottom" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <circle cx="12" cy="12" r="10" stroke-width="2"></circle>
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6l4 2" />
      </svg>
      Срок: {{ formatShortDate(task.due_date) }}
    </div>

    <!-- Boshqa info (comments, views, assigned) bo‘lsa, xuddi avvalgi misolda qo‘shish mumkin -->
  </div>
</template>

<script>
export default {
  name: "TaskCard",
  props: {
    task: {
      type: Object,
      required: true,
    },
  },
  emits: ['update-task', 'click', 'edit'],
  data() {
    return {
      // Agar completed qiymatini checkbox bilan bog‘lamoqchi bo‘lsangiz:
      localCompleted: this.task.completed || false,
    };
  },
  watch: {
    // Agar parent’dan task.completed o‘zgarsa, localCompleted ham yangilansin
    'task.completed'(newVal) {
      this.localCompleted = newVal;
    }
  },
  methods: {
    formatShortDate(dateStr) {
      const date = new Date(dateStr);
      if (isNaN(date)) return dateStr;
      const day = date.getDate();
      const monthNames = ['янв.', 'февр.', 'мар.', 'апр.', 'май', 'июн.', 'июл.', 'авг.', 'сент.', 'окт.', 'нояб.', 'дек.'];
      const month = monthNames[date.getMonth()] || '';
      return `${day} ${month}`;
    },
    formatDate(dateStr) {
      const date = new Date(dateStr);
      if (isNaN(date)) return dateStr;
      return date.toLocaleString();
    },
  },
};
</script>

<style scoped>
/* Qo‘shimcha uslublar kerak bo‘lsa qo‘shing */
</style>
