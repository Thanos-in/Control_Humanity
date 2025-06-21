<!-- TaskCard.vue -->
<template>
  <div class="bg-white p-4 rounded shadow">
    <h4 class="font-medium">{{ task.title }}</h4>
    <p class="text-sm text-gray-600" v-if="task.description">
      {{
        task.description.length > 50
          ? task.description.slice(0, 50) + "…"
          : task.description
      }}
    </p>
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
};
</script>

<style scoped>
/* Qo‘shimcha styling kerak bo‘lsa */
</style>
