<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-900 via-black to-gray-800 p-4">
    <div class="w-full max-w-xl bg-white/5 backdrop-blur-md rounded-2xl shadow-2xl p-8 border border-gray-700">
      <h2 class="text-3xl font-bold text-amber-400 text-center mb-8 tracking-wide">Welcome Back</h2>

      <form @submit.prevent="handleLogin" class="space-y-6">
        <div>
          <label for="username" class="block text-gray-200 font-medium mb-1">Username</label>
          <input
            v-model="credentials.username"
            id="username"
            type="text"
            placeholder="Enter your username"
            class="w-full p-3 rounded-lg bg-gray-800 text-gray-100 border border-gray-600 focus:outline-none focus:ring-2 focus:ring-amber-400"
          />
        </div>

        <div>
          <label for="password" class="block text-gray-200 font-medium mb-1">Password</label>
          <input
            v-model="credentials.password"
            id="password"
            type="password"
            placeholder="Enter your password"
            class="w-full p-3 rounded-lg bg-gray-800 text-gray-100 border border-gray-600 focus:outline-none focus:ring-2 focus:ring-amber-400"
          />
        </div>

        <div v-if="errorMessage" class="text-red-400 text-sm mt-2">
          {{ errorMessage }}
        </div>

        <button
          type="submit"
          class="w-full mt-2 bg-gradient-to-r from-amber-400 to-emerald-400 text-gray-900 font-semibold py-3 rounded-xl shadow-lg hover:from-amber-500 hover:to-emerald-500 transition duration-300"
          :disabled="loading"
        >
          <span v-if="loading">Logging in...</span>
          <span v-else>Login</span>
        </button>

        <button
          type="button"
          class="w-full bg-transparent border border-emerald-500 text-emerald-400 font-semibold py-3 rounded-xl hover:bg-emerald-500 hover:text-white transition mt-3"
          @click="handleSignup"
        >
          Sign Up
        </button>
      </form>
    </div>
  </div>
</template>


<script>
export default {
  name: 'Login',
  data() {
    return {
      credentials: {
        username: '',
        password: ''
      },
      loading: false,
      errorMessage: ''
    }
  },
  methods: {
    async handleLogin() {
      this.errorMessage = ''
      if (!this.credentials.username || !this.credentials.password) {
        this.errorMessage = 'Please enter both username and password.'
        return
      }

      try {
        this.loading = true
        await this.$store.dispatch('auth/login', {
          username: this.credentials.username,
          password: this.credentials.password
        })
        this.$router.push('/projects')
      } catch (err) {
        if (err.response && err.response.data) {
          this.errorMessage = err.response.data.detail || 'Login failed.'
        } else {
          this.errorMessage = 'Login failed. Please try again.'
        }
      } finally {
        this.loading = false
      }
    },
    handleSignup() {
      this.$router.push('/register')
    }
  }
}
</script>
