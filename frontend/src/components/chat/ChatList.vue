<template>
  <div>
    <h2 class="text-lg font-bold mb-4">Chat Rooms</h2>
    <ul>
      <li 
        v-for="room in rooms" 
        :key="room.id" 
        class="p-2 border-b hover:bg-gray-100 cursor-pointer"
        @click="goToChat(room.id)"
      >
        {{ room.id }} - {{ room.last_message?.content || 'No messages yet' }}
      </li>
    </ul>
  </div>
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
</script>
