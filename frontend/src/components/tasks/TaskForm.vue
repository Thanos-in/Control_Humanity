<template>
  <div class="fixed inset-0 bg-gradient-to-br from-blue-100 to-purple-200 flex items-center justify-center p-6 mt-20">
    <div class="bg-white p-10 rounded-3xl shadow-2xl w-full max-w-3xl overflow-y-auto max-h-full">
      <h2 class="text-4xl font-bold mb-8 text-center text-gray-800">Task Tafsilotlari</h2>
      
      <div class="space-y-6 text-gray-700 text-lg">
        <!-- Nomi -->
        <div>
          <p class="font-semibold mb-1">Nomi:</p>
          <p class="bg-gray-100 p-3 rounded-lg">{{ task.title }}</p>
        </div>

        <!-- Tavsif -->
        <div>
          <p class="font-semibold mb-1">Tavsif:</p>
          <p class="bg-gray-100 p-3 rounded-lg min-h-[120px] whitespace-pre-line">{{ task.description }}</p>
        </div>

        <!-- Berilgan -->
        <div>
          <p class="font-semibold mb-1">Berilgan:</p>
          <p class="bg-gray-100 p-3 rounded-lg">{{ task.user?.username || 'Noma’lum' }}</p>
        </div>

        <!-- Deadline -->
        <div>
          <p class="font-semibold mb-1">Deadline:</p>
          <p class="bg-gray-100 p-3 rounded-lg">{{ formatDate(task.due_date) }}</p>
        </div>

        <!-- Rang -->
        <div>
          <p class="font-semibold mb-1">Rang:</p>
          <div class="flex items-center space-x-4">
            <span class="inline-block w-10 h-10 rounded-full border-2" :style="{ backgroundColor: task.color }"></span>
            <span>{{ task.color }}</span>
          </div>
        </div>
      </div>

      <!-- Yopish tugmasi -->
      <div class="mt-10 flex justify-center">
        <button 
          @click="$emit('close')" 
          class="px-8 py-3 bg-gradient-to-r from-blue-400 to-purple-500 text-white rounded-full shadow-xl hover:scale-105 transform transition-transform duration-200"
        >
          Yopish
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

const route = useRoute();
const taskId = route.params.taskId;

const task = ref({
  title: '',
  description: '',
  user: { username: '' },
  due_date: '',
  color: '#000000'
});

function formatDate(dateStr) {
  if (!dateStr) return 'Noma’lum';
  const date = new Date(dateStr);
  return date.toLocaleDateString();
}

onMounted(() => {
  console.log('Task ID from route:', taskId);
  axios.get(`/api/tasks/${taskId}/`)
    .then(res => {
      task.value = res.data
    })
    .catch(err => {
      console.error('Task yuklanmadi:', err);
    });
});
</script>
