<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-700 via-indigo-800 to-purple-900 p-4">
    <div class="w-full max-w-md bg-white/10 backdrop-blur-lg rounded-2xl shadow-2xl p-8 border border-white/20">
      <h2 class="text-3xl font-bold text-white text-center mb-8 tracking-wide">Добро пожаловать!</h2>

      <form @submit.prevent="handleLogin" class="space-y-6">
        <div>
          <label for="username" class="block text-gray-200 font-medium mb-1">Имя пользователя</label>
          <input
            v-model="credentials.username"
            id="username"
            type="text"
            placeholder="Введите имя пользователя"
            class="w-full p-3 rounded-lg bg-gray-800 text-gray-100 border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-400"
          />
        </div>

        <div>
          <label for="password" class="block text-gray-200 font-medium mb-1">Пароль</label>
          <input
            v-model="credentials.password"
            id="password"
            type="password"
            placeholder="Введите свой пароль"
            class="w-full p-3 rounded-lg bg-gray-800 text-gray-100 border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-400"
          />
        </div>

        <div v-if="errorMessage" class="text-red-400 text-sm mt-2">
          {{ errorMessage }}
        </div>

        <button
          type="submit"
          class="w-full mt-2 bg-gradient-to-r from-purple-500 to-pink-500 text-white font-semibold py-3 rounded-xl shadow-lg hover:from-purple-600 hover:to-pink-600 transition duration-300"
          :disabled="loading"
        >
          <span v-if="loading">Загрузка...</span>
          <span v-else>Войти</span>
        </button>

        <button
          type="button"
          class="w-full bg-transparent border border-pink-400 text-pink-400 font-semibold py-3 rounded-xl hover:bg-pink-500 hover:text-white transition mt-3"
          @click="handleSignup"
        >
          Зарегистрироваться
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
        //await this.$store.dispatch('auth/login', {
        //  username: this.credentials.username,
        //  password: this.credentials.password
        //})
        //this.$router.push('/projects')
        const role = await this.$store.dispatch("auth/login", {
          username: this.credentials.username,
          password: this.credentials.password,
        });
        if (role === "employee") {
          this.$router.push("/taskstable");
        } else {
          this.$router.push("/projects");
        }
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
