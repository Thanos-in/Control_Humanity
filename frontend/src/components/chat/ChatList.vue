<template>
    <h2 class="text-3xl font-bold text-white mb-8">Chat Rooms</h2>
    <ul class="space-y-4">
      <li 
        v-for="room in rooms" 
        :key="room.id" 
        @click="goToChat(room.id)"
        class="bg-white bg-opacity-90 backdrop-blur-sm shadow-lg rounded-xl p-6 flex justify-between items-center cursor-pointer hover:scale-[1.02] transform transition"
      >
        <div>
          <h3 class="text-xl font-semibold text-gray-800">Room #{{ room.id }}</h3>
          <p class="text-gray-600 truncate max-w-[80vw]">
            {{ room.last_message?.content || 'No messages yet' }}
          </p>
        </div>
        <span class="text-sm text-gray-500">
          {{ formatTime(room.last_message?.timestamp) }}
        </span>
      </li>
    </ul>
</template>

<script setup>
import { onMounted, computed } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

const store = useStore()
const router = useRouter()

const rooms = computed(() => store.getters['chat/allRooms'])

onMounted(() => {
  store.dispatch('chat/fetchRooms')
})

const goToChat = (roomId) => {
  router.push(`/chat/${roomId}`)
}

const formatTime = (timestamp) => {
  if (!timestamp) return ''
  const date = new Date(timestamp)
  return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}
</script>
