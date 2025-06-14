<template>
  <div
    class="fixed inset-0 bg-gradient-to-br from-blue-100 to-purple-200 flex items-center justify-center p-6 mt-20">
    <div :class="['bg-white p-10 rounded-3xl shadow-2xl w-full max-w-3xl overflow-y-auto max-h-full transition-all',
        editing ? 'border-4 border-green-400' : 'border-none',
      ]">
      <div class="flex items-center justify-between mb-8">
        <h2 class="text-4xl font-bold text-gray-800">Task Tafsilotlari</h2>
        <!-- Edit / Close icon -->
        <button
          @click="toggleEdit"
          :class="[
            'p-2 rounded-full bg-white shadow hover:bg-gray-100 transition-colors',
            editing
              ? 'text-red-500 hover:text-red-600'
              : 'text-blue-500 hover:text-blue-600',
          ]"
          aria-label="Toggle Edit Mode"
        >
          <span v-if="!editing" class="text-2xl">✏️</span>
          <span v-else class="text-2xl">✖️</span>
        </button>
      </div>

      <!-- Detail or Form -->
      <div v-if="!editing" class="space-y-6 text-gray-700 text-lg">
        <div>
          <p class="font-semibold mb-1">Nomi:</p>
          <p class="bg-gray-100 p-3 rounded-lg">{{ task.title }}</p>
        </div>
        <div>
          <p class="font-semibold mb-1">Tavsif:</p>
          <p
            class="bg-gray-100 p-3 rounded-lg min-h-[120px] whitespace-pre-line"
          >
            {{ task.description }}
          </p>
        </div>
        <div>
          <p class="font-semibold mb-1">Berilgan:</p>
          <p class="bg-gray-100 p-3 rounded-lg">
            {{ task.user?.username || "Noma’lum" }}
          </p>
        </div>
        <div>
          <p class="font-semibold mb-1">Deadline:</p>
          <p class="bg-gray-100 p-3 rounded-lg">
            {{ formatDate(task.due_date) }}
          </p>
        </div>
        <div>
          <p class="font-semibold mb-1">Rang:</p>
          <div class="flex items-center space-x-4">
            <span
              class="inline-block w-10 h-10 rounded-full border-2"
              :style="{ backgroundColor: task.color }"
            ></span>
            <span>{{ task.color }}</span>
          </div>
        </div>
      </div>

      <form
        v-else
        @submit.prevent="submitEdit"
        class="space-y-6 text-gray-700 text-lg"
      >
        <div>
          <label class="font-semibold mb-1 block">Nomi:</label>
          <input
            v-model="edited.title"
            type="text"
            class="w-full bg-gray-100 p-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-300"
          />
        </div>
        <div>
          <label class="font-semibold mb-1 block">Tavsif:</label>
          <textarea
            v-model="edited.description"
            class="w-full bg-gray-100 p-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-300 min-h-[120px]"
          ></textarea>
        </div>
        <div>
          <label class="font-semibold mb-1 block">Deadline:</label>
          <input
            v-model="edited.due_date"
            type="date"
            class="w-full bg-gray-100 p-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-300"
          />
        </div>
        <div>
          <label class="font-semibold mb-1 block">Rang:</label>
          <input
            v-model="edited.color"
            type="color"
            class="w-12 h-12 p-0 border-0 focus:outline-none focus:ring-2 focus:ring-blue-300"
          />
        </div>
        <div class="flex space-x-4">
          <button
            type="submit"
            class="px-6 py-2 bg-green-500 text-white rounded-full shadow hover:bg-green-600 transition"
          >
            Saqlash
          </button>
          <button
            type="button"
            @click="cancelEdit"
            class="px-6 py-2 bg-gray-400 text-white rounded-full shadow hover:bg-gray-500 transition"
          >
            Bekor qilish
          </button>
        </div>
      </form>

      <!-- Actions -->
      <div class="mt-8 flex justify-center space-x-4">
        <button
          @click="confirmDelete"
          class="px-6 py-2 bg-red-500 text-white rounded-full shadow hover:bg-red-600 transition"
        >
          Delete
        </button>
        <button
          @click="closeModal"
          class="px-6 py-2 bg-blue-400 text-white rounded-full shadow hover:bg-blue-500 transition"
        >
          Close
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import axios from "axios";

const route = useRoute();
const router = useRouter();
const taskId = route.params.taskId;

const task = ref({
  title: "",
  description: "",
  user: { username: "" },
  due_date: "",
  color: "#000000",
});
const editing = ref(false);
const edited = ref({
  title: "",
  description: "",
  due_date: "",
  color: "#000000",
});

function formatDate(dateStr) {
  if (!dateStr) return "Noma’lum";
  return new Date(dateStr).toLocaleDateString();
}

function fetchTask() {
  axios
    .get(`/api/tasks/${taskId}/`)
    .then((res) => {
      task.value = res.data;
    })
    .catch((err) => {
      console.error("Task yuklanmadi:", err);
    });
}

function toggleEdit() {
  if (editing.value) {
    cancelEdit();
  } else {
    edited.value = {
      title: task.value.title,
      description: task.value.description,
      due_date: task.value.due_date?.split("T")[0] || "",
      color: task.value.color,
    };
    editing.value = true;
  }
}

function submitEdit() {
  axios
    .put(`/api/tasks/${taskId}/`, { ...edited.value })
    .then(() => {
      alert("Task updated");
      editing.value = false;
      router.push("/tasks");
      fetchTask();
    })
    .catch((err) => {
      console.error("Error:", err);
    });
}

function cancelEdit() {
  editing.value = false;
}

function confirmDelete() {
  if (confirm("Taskni o‘chirishni xohlaysizmi?")) {
    axios
      .delete(`/api/tasks/${taskId}/`)
      .then(() => {
        alert("Task deleted");
        router.back();
      })
      .catch((err) => {
        console.error("Error:", err);
      });
  }
}

function closeModal() {
  router.back();
}

onMounted(fetchTask);
</script>

<style scoped>
/* Qo'shimcha uslublar kerak bo'lsa shu yerda */
</style>