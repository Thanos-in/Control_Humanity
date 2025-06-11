<template>
  <div class="flex flex-col h-full">
    <!-- Xabarlar qismi -->
    <div class="flex-1 overflow-y-auto p-4 space-y-4">
      <div v-for="message in messages" :key="message.id"
           :class="message.sender.id === currentUser.id ? 'flex justify-end' : 'flex justify-start'">

        <!-- Agar boshqalar yuborgan bo‘lsa avatar -->
        <img v-if="message.sender.id !== currentUser.id" 
             class="w-8 h-8 rounded-full" 
             :src="message.sender.profile_picture || '/profiles/photo_2025-02-24_10-21-34.jpg'"
             alt="Avatar" />

        <!-- Xabar konteyneri -->
        <div :class="message.sender.id === currentUser.id ? 'bg-blue-500 text-white rounded-s-xl rounded-ee-xl' : 'bg-gray-100 text-gray-900 rounded-e-xl rounded-es-xl'"
             class="max-w-xs p-3">
          <div class="text-sm font-semibold mb-1">{{ message.sender.username }}</div>
          <p class="text-sm">{{ message.content }}</p>
          <div class="text-xs text-right text-gray-400">{{ formatTime(message.timestamp) }}</div>
        </div>

        <!-- Agar o‘zing yuborgan bo‘lsang avatar -->
        <img v-if="message.sender.id === currentUser.id" 
          class="w-8 h-8 rounded-full" 
          :src="message.sender.profile_picture || '/photo_2025-02-24_10-21-34.jpg'" 
          alt="Avatar" />
      </div>
    </div>

    <!-- Yozish qismi -->
    <div class="p-4 border-t flex items-center gap-2">
      <input v-model="newMessage" 
             type="text" 
             placeholder="Xabar yozing..." 
             class="flex-1 p-2 border rounded-lg outline-none" 
             @keyup.enter="sendMessage" />
      <button @click="sendMessage"
              class="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600">
        Jo‘natish
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useStore } from 'vuex'
import { useRoute } from 'vue-router'

const store = useStore()
const route = useRoute()

const messages = computed(() => store.state.chat.messages)
const currentUser = computed(() => store.state.auth.user)
const newMessage = ref('')

const formatTime = (timestamp) => {
  return new Date(timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

const sendMessage = async () => {
  if (!newMessage.value.trim()) return
  await store.dispatch('chat/sendMessage', { roomId: route.params.id, content: newMessage.value })
  newMessage.value = ''
}
</script>
