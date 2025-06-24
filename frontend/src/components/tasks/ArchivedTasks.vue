<template>
  <div class="relative overflow-x-auto shadow-md sm:rounded-lg">
    <table class="w-full text-sm text-left text-gray-500 dark:text-gray-400">
      <thead
        class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400"
      >
        <tr>
          <th scope="col" class="px-6 py-3">Задачи</th>
          <th scope="col" class="px-6 py-3">Период</th>
          <th scope="col" class="px-6 py-3">Статус</th>
          <th scope="col" class="px-6 py-3 text-right">Действия</th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="task in tasks"
          :key="task.id"
          class="bg-white border-b dark:bg-gray-800 dark:border-gray-700"
        >
          <!-- Задачи: task.title -->
          <td
            class="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white"
          >
            {{ task.title }}
          </td>
          <td class="px-6 py-4">
            {{ formatPeriod(task.created_at, task.due_date) }}
          </td>
          <td class="px-6 py-4">
            {{ task.status?.name || task.status?.title || "—" }}
          </td>
          <td class="px-6 py-4 text-right space-x-2">
            <button
              @click="goToTaskForm(task.id)"
              class="font-medium text-blue-600 dark:text-blue-500 hover:underline"
            >
              Просмотр
            </button>
          </td>
        </tr>

        <tr v-if="tasks.length === 0">
          <td colspan="4" class="px-6 py-4 text-center text-gray-500">
            Нет задач
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import TaskFormModal from "@/components/ui/AddTaskModal.vue";
import api from "@/utils/axios";
import { useRouter } from 'vue-router';

const tasks = ref([]);
const loading = ref(false);
const error = ref(null);
const router = useRouter();

const showEditModal = ref(false);
const selectedTask = ref(null);

  function goToTaskForm(taskId) {
      router.push({ path: `/taskform/${taskId}`, query: { archived: '1' } });
  }

async function fetchTasks() {
  loading.value = true;
  error.value = null;
  try {
    const response = await api.get("/tasks/archivedtasks/");
    tasks.value = response.data;
    // tasks.value = response.data.results
  } catch (err) {
    console.error(err);
    error.value = "Ошибка при загрузке задач";
  } finally {
    loading.value = false;
  }
}

function formatDate(dateStr) {
  if (!dateStr) return "-";
  const d = new Date(dateStr);
  // toLocaleDateString mos bo'lsa:
  return d.toLocaleDateString("ru-RU", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
  });
}
function formatPeriod(createdAt, dueDate) {
  const from = formatDate(createdAt);
  const to = dueDate ? formatDate(dueDate) : "-";
  return `${from} → ${to}`;
}

function onEdit(task) {
  selectedTask.value = { ...task };
  showEditModal.value = true;
}
function closeEditModal() {
  showEditModal.value = false;
  selectedTask.value = null;
}
function onTaskSaved() {
  showEditModal.value = false;
  selectedTask.value = null;
  fetchTasks();
}

onMounted(() => {
  fetchTasks();
});
</script>

