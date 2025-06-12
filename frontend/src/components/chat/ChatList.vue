<template>
  <div>
    <!-- Header va New Chat Room tugmasi -->
    <div class="flex items-center justify-between mb-8">
      <h2 class="text-3xl font-bold text-white">Chat Rooms</h2>
      <button @click="showCreateModal = true" class="bg-green-500 text-white px-4 py-2 rounded-lg hover:bg-green-600 transition">
        + New Chat Room
      </button>
    </div>

    <!-- Create Chat Room Modal -->
    <div v-if="showCreateModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
      <div class="bg-white p-6 rounded-xl shadow-lg w-full max-w-md">
        <h3 class="text-xl font-semibold mb-4">Create Chat Room</h3>
        
        <label class="block mb-2 text-gray-700">Select Participants:</label>
        <ul class="max-h-60 overflow-y-auto space-y-2">
          <li 
            v-for="user in users" 
            :key="user.id" 
            @click="toggleUser(user.id)"
            class="flex items-center space-x-3 p-2 rounded cursor-pointer hover:bg-gray-100 transition"
          >
            <input 
              type="checkbox" 
              :checked="selectedUsers.includes(user.id)" 
              @change.stop
            />
            <span>{{ user.username }}</span>
          </li>
        </ul>

        <div class="flex justify-end space-x-2 mt-4">
          <button @click="closeCreateModal" class="px-4 py-2 bg-gray-300 rounded hover:bg-gray-400">Cancel</button>
          <button @click="createRoom" class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">Create</button>
        </div>
      </div>
    </div>

    <!-- Chat Rooms List -->
    <ul class="space-y-4">
      <li 
        v-for="room in rooms" 
        :key="room.id" 
        @click="goToChat(room.id)"
        class="relative bg-white bg-opacity-90 backdrop-blur-sm shadow-lg rounded-xl p-6 flex justify-between items-center cursor-pointer hover:scale-[1.02] transform transition"
      >
        <div>
          <h3 class="text-xl font-semibold text-gray-800">Room #{{ room.id }}</h3>
          <p class="text-gray-600 truncate max-w-[80vw]">
            {{ room.last_message?.content || 'No messages yet' }}
          </p>
        </div>
        <div class="flex items-center space-x-4">
          <span class="text-sm text-gray-500">{{ formatTime(room.last_message?.timestamp) }}</span>
          <span 
            v-if="room.unread_count" 
            class="inline-block bg-red-500 text-white text-xs font-semibold px-2 py-1 rounded-full"
          >
            {{ room.unread_count }}
          </span>
        </div>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

const store = useStore()
const router = useRouter()

const rooms = computed(() => store.getters['chat/allRooms'])
const users = ref([])
const selectedUsers = ref([])
const showCreateModal = ref(false)

onMounted(async () => {
  await store.dispatch('chat/fetchRooms')
  const res = await store.dispatch('chat/fetchUsers')
  users.value = res
})

const toggleUser = (userId) => {
  if (selectedUsers.value.includes(userId)) {
    selectedUsers.value = selectedUsers.value.filter(id => id !== userId)
  } else {
    selectedUsers.value.push(userId)
  }
}

const closeCreateModal = () => {
  showCreateModal.value = false
  selectedUsers.value = []
}

const createRoom = async () => {
  if (!selectedUsers.value.length) return alert("Select at least one user.")
  const newRoom = await store.dispatch('chat/createRoom', selectedUsers.value)
  closeCreateModal()
  router.push(`/chat/${newRoom.id}`)
}

const goToChat = (roomId) => {
  router.push(`/chat/${roomId}`)
}

const formatTime = (timestamp) => {
  if (!timestamp) return ''
  return new Date(timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}
</script>
