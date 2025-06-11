<template>
  <div class="flex flex-col h-full">
    <!-- Xabarlar qismi -->
    <div class="flex-1 overflow-y-auto p-4 space-y-4">
      <div v-for="message in messages" :key="message.id"
           :class="message.sender.id === currentUser.id ? 'flex justify-end' : 'flex justify-start'">

        <!-- Agar boshqalar yuborgan bo‘lsa avatar -->
        <div class="flex items-start gap-2.5" v-if="message.sender.id !== currentUser.id">
          <img class="w-8 h-8 rounded-full" 
               :src="message.sender.profile_picture || defaultAvatar" 
               alt="Avatar" />

          <div class="flex flex-col w-full max-w-[320px] leading-1.5 p-4 border-gray-200 bg-gray-100 rounded-e-xl rounded-es-xl">
            <div class="flex items-center space-x-2">
              <span class="text-sm font-semibold text-gray-900">{{ message.sender.username }}</span>
              <span class="text-sm text-gray-500">{{ formatTime(message.timestamp) }}</span>
            </div>
            <p class="text-sm text-gray-900 py-2.5">{{ message.content }}</p>
            <span class="text-sm text-gray-500">Delivered</span>
          </div>

          <!-- Dropdown menyu -->
          <div class="relative">
            <button @click="toggleDropdown(message.id)" class="p-2 rounded-lg hover:bg-gray-200">
              <svg class="w-4 h-4 text-gray-500" fill="currentColor" viewBox="0 0 4 15">
                <path d="M3.5 1.5a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0Zm0 6.041a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0Zm0 5.959a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0Z"/>
              </svg>
            </button>
            <div v-if="dropdownOpen === message.id" class="absolute right-0 z-10 mt-2 bg-white rounded-lg shadow-lg w-40">
              <ul class="py-2 text-sm text-gray-700">
                <li><a href="#" class="block px-4 py-2 hover:bg-gray-100">Reply</a></li>
                <li><a href="#" class="block px-4 py-2 hover:bg-gray-100">Forward</a></li>
                <li><a href="#" class="block px-4 py-2 hover:bg-gray-100">Copy</a></li>
                <li><a href="#" class="block px-4 py-2 hover:bg-gray-100">Report</a></li>
                <li>
                  <button @click="deleteMessage(message.id)" class="w-full text-left block px-4 py-2 hover:bg-gray-100">
                    Delete
                  </button>
                </li>
              </ul>
            </div>
          </div>
        </div>

        <!-- O'z xabaring bo‘lsa -->
        <div class="flex items-start gap-2.5" v-else>
          <div class="relative">
            <button @click="toggleDropdown(message.id)" class="p-2 rounded-lg hover:bg-gray-200">
              <svg class="w-4 h-4 text-gray-500" fill="currentColor" viewBox="0 0 4 15">
                <path d="M3.5 1.5a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0Zm0 6.041a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0Zm0 5.959a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0Z"/>
              </svg>
            </button>
            <div v-if="dropdownOpen === message.id" class="absolute right-0 z-10 mt-2 bg-white rounded-lg shadow-lg w-40">
              <ul class="py-2 text-sm text-gray-700">
                <li><a href="#" class="block px-4 py-2 hover:bg-gray-100">Reply</a></li>
                <li><a href="#" class="block px-4 py-2 hover:bg-gray-100">Forward</a></li>
                <li><a href="#" class="block px-4 py-2 hover:bg-gray-100">Copy</a></li>
                <li><a href="#" class="block px-4 py-2 hover:bg-gray-100">Report</a></li>
                <li>
                  <button @click="deleteMessage(message.id)" class="w-full text-left block px-4 py-2 hover:bg-gray-100">
                    Delete
                  </button>
                </li>
              </ul>
            </div>
          </div>

          <div class="flex flex-col w-full max-w-[320px] leading-1.5 p-4 border-gray-200 bg-blue-500 text-white rounded-s-xl rounded-ee-xl">
            <div class="flex items-center space-x-2">
              <span class="text-sm font-semibold">{{ message.sender.username }}</span>
              <span class="text-sm">{{ formatTime(message.timestamp) }}</span>
            </div>
            <p class="text-sm py-2.5">{{ message.content }}</p>
            <span class="text-sm">Delivered</span>
          </div>

          <img class="w-8 h-8 rounded-full" 
               :src="message.sender.profile_picture || defaultAvatar" 
               alt="Avatar" />
        </div>

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

  <!-- DELETE MODAL -->
  <div v-if="showDeleteModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
    <div class="bg-white p-6 rounded-lg shadow-lg w-80">
      <h2 class="text-lg font-semibold mb-4">Xabarni o‘chirish</h2>
      <p class="text-gray-700 mb-4">Rostdan ham bu xabarni o‘chirishni xohlaysizmi?</p>
      <div class="flex justify-end space-x-2">
        <button @click="closeDeleteModal" class="px-4 py-2 bg-gray-300 rounded hover:bg-gray-400">Bekor qilish</button>
        <button @click="confirmDelete" class="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600">O‘chirish</button>
      </div>
    </div>
  </div>

</template>

<script setup>
import { computed, ref, onMounted } from 'vue'
import { useStore } from 'vuex'
import { useRoute } from 'vue-router'
import defaultAvatar from '../../assets/Default.png'

const store = useStore()
const route = useRoute()

const messages = computed(() => store.state.chat.messages)
const currentUser = computed(() => store.state.auth.user)
const newMessage = ref('')
const dropdownOpen = ref(null)

const showDeleteModal = ref(false)
const messageToDelete = ref(null)


const formatTime = (timestamp) => {
  return new Date(timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

const sendMessage = async () => {
  if (!newMessage.value.trim()) return
  await store.dispatch('chat/sendMessage', { roomId: route.params.id, content: newMessage.value })
  newMessage.value = ''
}

const toggleDropdown = (id) => {
  dropdownOpen.value = dropdownOpen.value === id ? null : id
}

const openDeleteModal = (id) => {
  messageToDelete.value = id
  showDeleteModal.value = true
  dropdownOpen.value = null // Dropdown yopiladi
}

const closeDeleteModal = () => {
  showDeleteModal.value = false
  messageToDelete.value = null
}

const confirmDelete = async () => {
  try {
    await store.dispatch('chat/deleteMessage', { messageId: messageToDelete.value, roomId: route.params.id })
    closeDeleteModal()
  } catch (error) {
    alert('Xatolik yuz berdi: ' + error.message)
  }
}

const deleteMessage = (id) => {
  openDeleteModal(id)
}

onMounted(() => {
  store.dispatch('chat/fetchMessages', route.params.id)
})
</script>
