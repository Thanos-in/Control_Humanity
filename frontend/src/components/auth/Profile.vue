<template>
  <div class="max-w-2xl mx-auto p-6 bg-white rounded-lg shadow-md">
    <h1 class="text-2xl font-semibold mb-4">User Profile</h1>

    <form @submit.prevent>
      <!-- Username -->
      <div class="mb-4">
        <label class="block text-sm font-medium text-gray-700 mb-1" for="username">Username</label>
        <input
          v-model="profile.username"
          id="username"
          type="text"
          class="w-full px-3 py-2 border rounded focus:outline-none focus:ring"
          :disabled="!canEditOwn"
        />
      </div>

      <!-- Email -->
      <div class="mb-4">
        <label class="block text-sm font-medium text-gray-700 mb-1" for="email">Email</label>
        <input
          v-model="profile.email"
          id="email"
          type="email"
          class="w-full px-3 py-2 border rounded focus:outline-none focus:ring"
          :disabled="!canEditOwn"
        />
      </div>

      <!-- First/Last Name -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1" for="first_name">First Name</label>
          <input
            v-model="profile.first_name"
            id="first_name"
            type="text"
            class="w-full px-3 py-2 border rounded focus:outline-none focus:ring"
            :disabled="!canEditOwn"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1" for="last_name">Last Name</label>
          <input
            v-model="profile.last_name"
            id="last_name"
            type="text"
            class="w-full px-3 py-2 border rounded focus:outline-none focus:ring"
            :disabled="!canEditOwn"
          />
        </div>
      </div>

      <!-- Role -->
      <div class="mb-4">
        <label class="block text-sm font-medium text-gray-700 mb-1" for="role">Role</label>
        <select
          v-model="profile.role"
          id="role"
          class="w-full px-3 py-2 border rounded focus:outline-none focus:ring"
          :disabled="!canEditRole"
        >
          <option value="employee">Employee</option>
          <option value="manager">Manager</option>
          <option value="director">Director</option>
        </select>
      </div>

      <!-- Action Buttons -->
      <div class="flex space-x-4">
        <!-- Save Profile (only for self) -->
        <button
          v-if="canEditOwn"
          @click="saveProfile"
          type="button"
          class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
        >
          Save Profile
        </button>

        <!-- Save Role (only for director editing others) -->
        <button
          v-if="canEditRole"
          @click="saveRole"
          type="button"
          class="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600"
        >
          Save Role
        </button>
      </div>
    </form>

    <p v-if="error" class="mt-4 text-red-600">{{ error }}</p>
    <p v-if="success" class="mt-4 text-green-600">{{ success }}</p>
  </div>
</template>

<script>
import axios from 'axios'
import { mapState } from 'vuex'

export default {
  name: 'ProfileView',
  data() {
    return {
      profile: {},
      error: '',
      success: ''
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
      // user or manager editing own profile: canEditOwn true
      return this.isSelf
    },
    canEditRole() {
      // director editing others
      return this.isDirector && !this.isSelf
    }
  },
  async created() {
    try {
      const id = this.$route.params.userId
      const response = await axios.get(`/api/users/${id}/`)
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
        await axios.patch(`/api/users/${this.profile.id}/`, {
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
        await axios.patch(`/api/users/${this.profile.id}/`, {
          role: this.profile.role
        })
        this.success = 'Role updated successfully.'
      } catch (e) {
        this.error = 'Failed to update role.'
      }
    }
  }
}
</script>
