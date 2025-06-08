<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-900 via-black to-gray-800 p-4">
    <div class="w-full max-w-xl bg-white/5 backdrop-blur-md rounded-2xl shadow-2xl p-8 border border-gray-700">
      <h2 class="text-3xl font-bold text-amber-400 text-center mb-8 tracking-wide">Create Your Account</h2>

      <form @submit.prevent="handleRegister" class="space-y-5">
        <div>
          <label for="username" class="block text-gray-200 font-medium mb-1">Username</label>
          <input
            v-model="form.username"
            id="username"
            type="text"
            placeholder="Enter your username"
            class="w-full p-3 rounded-lg bg-gray-800 text-gray-100 border border-gray-600 focus:outline-none focus:ring-2 focus:ring-amber-400"
          />
        </div>

        <div>
          <label for="email" class="block text-gray-200 font-medium mb-1">Email</label>
          <input
            v-model="form.email"
            id="email"
            type="email"
            placeholder="Enter your email"
            class="w-full p-3 rounded-lg bg-gray-800 text-gray-100 border border-gray-600 focus:outline-none focus:ring-2 focus:ring-amber-400"
          />
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label for="first_name" class="block text-gray-200 font-medium mb-1">First Name</label>
            <input
              v-model="form.first_name"
              id="first_name"
              type="text"
              placeholder="First name"
              class="w-full p-3 rounded-lg bg-gray-800 text-gray-100 border border-gray-600 focus:outline-none focus:ring-2 focus:ring-amber-400"
            />
          </div>
          <div>
            <label for="last_name" class="block text-gray-200 font-medium mb-1">Last Name</label>
            <input
              v-model="form.last_name"
              id="last_name"
              type="text"
              placeholder="Last name"
              class="w-full p-3 rounded-lg bg-gray-800 text-gray-100 border border-gray-600 focus:outline-none focus:ring-2 focus:ring-amber-400"
            />
          </div>
        </div>

        <div>
          <label for="role" class="block text-gray-200 font-medium mb-1">Role</label>
          <select
            v-model="form.role"
            id="role"
            disabled
            class="w-full p-3 rounded-lg bg-gray-700 text-gray-300 border border-gray-600 cursor-not-allowed"
          >
            <option value="employee" selected>Employee</option>
          </select>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label for="password" class="block text-gray-200 font-medium mb-1">Password</label>
            <input
              v-model="form.password"
              id="password"
              type="password"
              placeholder="Password"
              class="w-full p-3 rounded-lg bg-gray-800 text-gray-100 border border-gray-600 focus:outline-none focus:ring-2 focus:ring-amber-400"
            />
          </div>
          <div>
            <label for="password2" class="block text-gray-200 font-medium mb-1">Confirm Password</label>
            <input
              v-model="form.password2"
              id="password2"
              type="password"
              placeholder="Repeat password"
              class="w-full p-3 rounded-lg bg-gray-800 text-gray-100 border border-gray-600 focus:outline-none focus:ring-2 focus:ring-amber-400"
            />
          </div>
        </div>

        <div v-if="errorMessage" class="text-red-400 text-sm mt-2">
          {{ errorMessage }}
        </div>

        <button
          type="submit"
          :disabled="loading"
          class="w-full mt-4 bg-gradient-to-r from-amber-400 to-emerald-400 text-gray-900 font-semibold py-3 rounded-xl shadow-lg hover:from-amber-500 hover:to-emerald-500 transition duration-300"
        >
          <span v-if="loading">Registering...</span>
          <span v-else>Sign Up</span>
        </button>
      </form>
    </div>
  </div>
</template>



<script>
export default {
  name: 'Register',
  data() {
    return {
      form: {
        username: '',
        email: '',
        first_name: '',
        last_name: '',
        role: 'employee',
        password: '',
        password2: ''
      },
      loading: false,
      errorMessage: ''
    }
  },
  methods: {
    async handleRegister() {
      this.errorMessage = ''

      // Basic validation
      if (
        !this.form.username ||
        !this.form.email ||
        !this.form.first_name ||
        !this.form.last_name ||
        !this.form.role ||
        !this.form.password ||
        !this.form.password2
      ) {
        this.errorMessage = 'All fields are required.'
        return
      }
      if (this.form.password !== this.form.password2) {
        this.errorMessage = 'Passwords do not match.'
        return
      }

      try {
        this.loading = true
        // Dispatch namespaced auth/register action
        await this.$store.dispatch('auth/register', {
          username: this.form.username,
          email: this.form.email,
          first_name: this.form.first_name,
          last_name: this.form.last_name,
          role: this.form.role,
          password: this.form.password,
          password2: this.form.password2
        })
        // After successful registration (and login), redirect to /projects
        this.$router.push('/projects')
      } catch (err) {
        // Display server-side validation errors if available
        if (err.response && err.response.data) {
          // Might receive a dictionary of field errors, or a "detail" key
          const data = err.response.data
          if (typeof data === 'object') {
            // Concatenate all error messages
            this.errorMessage = Object.values(data)
              .flat()
              .join(' ')
          } else {
            this.errorMessage = data || 'Registration failed.'
          }
        } else {
          this.errorMessage = 'Registration failed. Please try again.'
        }
      } finally {
        this.loading = false
      }
    }
  }
}
</script>
