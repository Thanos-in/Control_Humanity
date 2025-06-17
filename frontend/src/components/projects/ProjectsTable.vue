<template>
  <div class="relative overflow-x-auto shadow-md sm:rounded-lg">
    <table class="w-full text-sm text-left text-gray-500 dark:text-gray-400">
      <thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
        <tr>
          <th class="w-4 p-4"></th>
          <th class="px-6 py-3">Проект / Модуль / Задача</th>
          <th class="px-6 py-3">Ответственный</th>
          <th class="px-6 py-3">Период</th>
          <th class="px-6 py-3">Статус</th>
          <th class="px-6 py-3">Действия</th>
        </tr>
      </thead>
      <tbody>
        <template v-for="proj in projects" :key="proj.id">
          <!-- Project -->
          <tr class="bg-white border-b hover:bg-gray-50">
            <td class="p-4">
              <svg
                @click="toggleExpand(proj.id)"
                class="w-5 h-5 cursor-pointer transition-transform"
                :class="{ 'rotate-180': expandedProjects.includes(proj.id) }"
                fill="none" stroke="currentColor" viewBox="0 0 24 24"
              >
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M19 9l-7 7-7-7" />
              </svg>
            </td>
            <td class="px-6 py-4 font-semibold">{{ proj.name }}</td>
            <td class="px-6 py-4">{{ proj.manager?.username || '-' }}</td>
            <td class="px-6 py-4">{{ proj.period }}</td>
            <td class="px-6 py-4">—</td>
            <td class="px-6 py-4">
              <a href="#" class="text-blue-500 hover:underline">Edit</a>
            </td>
          </tr>

          <!-- Modules -->
          <template v-if="expandedProjects.includes(proj.id)">
            <template v-for="mod in proj.modules" :key="mod.id">
              <tr class="bg-gray-50 border-b">
                <td></td>
                <td class="px-10 py-3 font-medium">
                  <div class="flex items-center gap-2 cursor-pointer" @click="toggleModule(mod.id)">
                    <svg
                      class="w-4 h-4 transition-transform"
                      :class="{ 'rotate-180': expandedModules.includes(mod.id) }"
                      fill="none" stroke="currentColor" viewBox="0 0 24 24"
                    >
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M19 9l-7 7-7-7" />
                    </svg>
                    {{ mod.name }}
                  </div>
                </td>
                <td colspan="4"></td>
              </tr>

              <!-- Tasks -->
              <template v-if="expandedModules.includes(mod.id)">
                <tr
                  v-for="task in mod.tasks"
                  :key="task.id"
                  class="bg-white border-b"
                >
                  <td></td>
                  <td class="pl-16 pr-6 py-2">
                    📌 {{ task.title }}
                  </td>
                  <td class="px-6 py-2">{{ task.assigned_to?.username || '-' }}</td>
                  <td class="px-6 py-2">{{ formatPeriod(task.created_at, task.due_date) }}</td>
                  <td class="px-6 py-2">{{ statusLabel(task.status.name) }}</td>
                  <td class="px-6 py-2">
                    <a href="#" class="text-blue-500 hover:underline">Edit</a>
                  </td>
                </tr>
              </template>
            </template>
          </template>
        </template>
      </tbody>
    </table>
  </div>
</template>

<script>
import api from '@/utils/axios';

export default {
  data() {
    return {
      expandedProjects: [],
      expandedModules: [],
      projects: [],
    };
  },
  async created() {
    try {
      const { data } = await api.get('/projects/');
      this.projects = data;
    } catch (e) {
      console.error('Проекты не загружены', e);
    }
  },
  methods: {
    toggleExpand(id) {
      const i = this.expandedProjects.indexOf(id);
      i === -1 ? this.expandedProjects.push(id) : this.expandedProjects.splice(i, 1);
    },
    toggleModule(id) {
      const i = this.expandedModules.indexOf(id);
      i === -1 ? this.expandedModules.push(id) : this.expandedModules.splice(i, 1);
    },
    statusLabel(status) {
      const map = {
        done: 'Завершен',
        in_progress: 'В процессе',
        todo: 'Не начат',
      };
      return map[status] || status;
    },
    formatPeriod(start, end) {
      const s = this.formatDate(start);
      const e = this.formatDate(end);
      return `${s} — ${e}`;
    },
    formatDate(dateStr) {
      if (!dateStr) return '?';
      return new Date(dateStr).toLocaleDateString('ru-RU');
    },
  },
};
</script>

<style scoped>
.rotate-180 {
  transform: rotate(180deg);
}
</style>
