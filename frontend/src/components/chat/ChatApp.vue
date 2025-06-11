<template>
  <div class="flex h-screen">
    <aside class="w-1/3 border-r overflow-auto">
      <ChatList 
        :chats="rooms" 
        @chat-selected="handleChatSelect" 
      />
    </aside>
    <main class="flex-1 overflow-auto">
      <ChatWindow 
        :messages="messages" 
      />
    </main>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useStore } from 'vuex'
import ChatList from './ChatList.vue'
import ChatWindow from './ChatWindow.vue'

const store = useStore()

// Vuex orqali computed qiymatlar
const rooms = computed(() => store.getters['chat/allRooms'])
const messages = computed(() => store.getters['chat/allMessages'])

// Boshlang'ich yuklash
onMounted(() => {
  store.dispatch('chat/fetchRooms')
})

// Chat tanlanganda xabarlarni olish
function handleChatSelect(roomId) {
  store.dispatch('chat/fetchMessages', roomId)
}
</script>
