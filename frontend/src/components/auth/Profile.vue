<template>
  <div class="min-h-screen flex items-center justify-center p-6" style="background: linear-gradient(135deg, #667eea, #764ba2);">
    <div class="w-full max-w-2xl bg-white/10 backdrop-blur-md rounded-2xl shadow-xl p-8 border border-white/20">
      
      <!-- Profile Photo -->
      <div class="flex justify-center mb-6">
        <img
          :src="profile.profile_picture || defaultAvatar"
          alt="Avatar"
          class="w-24 h-24 rounded-full border-4 border-white object-cover 
         transition-all duration-200 ease-in-out 
         hover:w-28 hover:h-28 hover:shadow-lg"
        />
      </div>

      <h1 v-if="profile.username !== ''" class="text-3xl font-bold text-white text-center mb-8">Профиль  {{ profile.username }}а</h1>      
      <h1 v-if="profile.username == ''" class="text-3xl font-bold text-white text-center mb-8">User profile</h1>

      <form @submit.prevent class="space-y-6">
        <!-- Username -->
        <div>
          <label class="block text-sm font-medium text-white mb-1" for="username">Имя пользователя</label>
          <input
            v-model="profile.username"
            id="username"
            type="text"
            class="w-full px-4 py-2 bg-white/10 text-white border border-white/20 rounded-lg focus:outline-none focus:ring-2 focus:ring-yellow-300"
            :disabled="!canEditOwn"
          />
        </div>

        <!-- Email -->
        <div>
          <label class="block text-sm font-medium text-white mb-1" for="email">Email</label>
          <input
            v-model="profile.email"
            id="email"
            type="email"
            class="w-full px-4 py-2 bg-white/10 text-white border border-white/20 rounded-lg focus:outline-none focus:ring-2 focus:ring-yellow-300"
            :disabled="!canEditOwn"
          />
        </div>

        <!-- First & Last Name -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label class="block text-sm font-medium text-white mb-1" for="first_name">Имя</label>
            <input
              v-model="profile.first_name"
              id="first_name"
              type="text"
              class="w-full px-4 py-2 bg-white/10 text-white border border-white/20 rounded-lg focus:outline-none focus:ring-2 focus:ring-yellow-300"
              :disabled="!canEditOwn"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-white mb-1" for="last_name">Фамилия</label>
            <input
              v-model="profile.last_name"
              id="last_name"
              type="text"
              class="w-full px-4 py-2 bg-white/10 text-white border border-white/20 rounded-lg focus:outline-none focus:ring-2 focus:ring-yellow-300"
              :disabled="!canEditOwn"
            />
          </div>
        </div>

        <!-- Role -->
        <div>
          <label class="block text-sm font-medium text-white mb-1" for="role">Роль</label>
          <select
            v-model="profile.role"
            id="role"
            class="w-full px-4 py-2 bg-white/10 text-black border border-white/20 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-300"
            :disabled="!canEditRole"
          >
            <option value="employee">Employee</option>
            <option value="manager">Manager</option>
            <option value="Admin">Admin</option>
            <option value="director">Director</option>
          </select>
        </div>

        <!-- Action Buttons -->
        <div class="flex flex-wrap gap-4 mt-6">
          <button
            v-if="canEditOwn"
            @click="saveProfile"
            type="button"
            class="px-6 py-2 bg-yellow-300 text-gray-900 font-semibold rounded-lg hover:bg-yellow-400 transition duration-300"
          >
            Сохранить
          </button>

          <button
            v-if="canEditRole"
            @click="saveRole"
            type="button"
            class="px-6 py-2 bg-green-300 text-gray-900 font-semibold rounded-lg hover:bg-green-400 transition duration-300"
          >
            Сохранить
          </button>
          <button 
          @click="closeModal" 
          class="px-6 py-2 bg-red-300 text-gray-900 font-semibold rounded-lg hover:bg-red-400 transition duration-300">
          Закрыть
          </button>
        </div>
      </form>

      <!-- Messages -->
      <p v-if="error" class="mt-6 text-red-300 text-sm text-center">{{ error }}</p>
      <p v-if="success" class="mt-6 text-green-300 text-sm text-center">{{ success }}</p>
    </div>
  </div>
</template>

<script>
import api from '@/utils/axios'
import { mapState } from 'vuex'
import defaultAvatar from '../../assets/Default.png'

export default {
  name: 'ProfileView',
  data() {
    return {
      profile: {},
      error: '',
      success: '',
      defaultAvatar
    }
  },
  computed: {
    ...mapState('auth', ['user']),
    isSelf() {
      return this.user.id === this.profile.id
    },
    isDirector() {
      return this.user.role === 'director'
    },
    canEditOwn() {
      return this.isSelf
    },
    canEditRole() {
      return this.isDirector && !this.isSelf
    }
  },
  async created() {
    try {
      const id = this.$route.params.userId
      const response = await api.get(`/auth/profiles/${id}/`)
      this.profile = response.data
    } catch (e) {
      this.error = 'Failed to load profile.'
    }
  },
  methods: {
    async saveProfile() {
      this.error = ''
      this.success = ''
      try {
        await api.patch(`/auth/profiles/${this.profile.id}/`, {
          username: this.profile.username,
          email: this.profile.email,
          first_name: this.profile.first_name,
          last_name: this.profile.last_name
        })
        this.success = 'Profile updated successfully.'
      } catch (e) {
        this.error = 'Failed to update profile.'
      }
    },
    async saveRole() {
      this.error = ''
      this.success = ''
      try {
        await api.patch(`/auth/profiles/${this.profile.id}/`, {
          role: this.profile.role
        })
        this.success = 'Role updated successfully.'
      } catch (e) {
        this.error = 'Failed to update role.'
      }
    },

  closeModal() {
    this.$router.back();  // 'this' orqali chaqirilsin
    }
  }
}
</script>
