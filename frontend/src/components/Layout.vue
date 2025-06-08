<template>
  <div class="h-screen flex flex-col bg-pink-50">
    <!-- Navbar -->
    <header class="fixed top-0 left-0 right-0 bg-white/90 backdrop-blur-md border-b border-gray-200 z-50">
  <div class="flex items-center justify-between px-6 py-4">
    <!-- Brand flush left -->
    <div class="flex items-center space-x-4">
      <button @click="toggleSidebar" class="p-2 rounded-md bg-gray-100 hover:bg-gray-200 transition">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
        </svg>
      </button>
      <h1 class="text-2xl font-semibold text-gray-800">MyTaskManager</h1>
    </div>

    <!-- Nav flush right -->
    <nav class="space-x-4 relative">
      <router-link to="/projects" class="px-3 py-1 text-gray-700 hover:text-pink-500 transition">Projects</router-link>
      <router-link to="/tasks"    class="px-3 py-1 text-gray-700 hover:text-pink-500 transition">Tasks</router-link>
      <router-link to="/chat"     class="px-3 py-1 text-gray-700 hover:text-pink-500 transition">Chat</router-link>
      <router-link to="/ratings"  class="px-3 py-1 text-gray-700 hover:text-pink-500 transition">Ratings</router-link>
      
      <button @click="toggleDropdown" id="dropdownDefaultButton"
      class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center inline-flex items-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
      type="button">
      {{ currentLanguage }}
      <svg class="w-2.5 h-2.5 ms-3" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 10 6">
        <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
          d="m1 1 4 4 4-4" />
      </svg>
    </button>

    <!-- Dropdown menu -->
    <div v-show="isDropdownOpen"
    class="absolute right-20 mt-2 z-10 bg-white divide-y divide-gray-100 rounded-lg shadow-sm w-44 dark:bg-gray-700">
      <ul class="py-2 text-sm text-gray-700 dark:text-gray-200">
        <li>
          <a href="#" @click.prevent="setLanguage('Eng')"
            class="block px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white">Eng</a>
        </li>
        <li>
          <a href="#" @click.prevent="setLanguage('Ru')"
            class="block px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white">Ru</a>
        </li>
      </ul>
   </div>
      <router-link
        v-if="$store.state.auth.token"
        :to="`/profile/${$store.state.auth.user.id}`"
        class="px-3 py-1 bg-pink-200 text-pink-700 rounded hover:bg-pink-300 transition"
      >My Profile</router-link>

    </nav>
  </div>
</header>

    <!-- Layout Surrounding container -->
    <div class="flex flex-1 pt-[68px] overflow-hidden">
      <!-- Sidebar -->
      <aside
        v-if="showSidebar"
        class="fixed top-[68px] left-0 h-[calc(100vh-68px)] w-64 bg-white/90 backdrop-blur-md border-r border-gray-200 shadow-inner z-40"
      >
        <nav class="mt-6 px-4 space-y-4">
          <router-link to="/projects" class="block text-gray-800 hover:text-pink-500">Projects</router-link>
          <router-link to="/tasks"    class="block text-gray-800 hover:text-pink-500">Tasks</router-link>
          <router-link to="/chat"     class="block text-gray-800 hover:text-pink-500">Chat</router-link>
          <router-link to="/ratings"  class="block text-gray-800 hover:text-pink-500">Ratings</router-link>
        </nav>
      </aside>

      <!-- Page Content -->
      <main
        class="flex-1 overflow-auto p-6 ml-0"
        :class="{ 'ml-64': showSidebar }"
        
      >
        <router-view />
      </main>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Layout',
  data() {
    return {
      showSidebar: true,
      isDropdownOpen: false,
      currentLanguage: 'Eng'
  }
  },
  methods: {
    toggleSidebar() {
      this.showSidebar = !this.showSidebar
    },
    toggleDropdown() {
      this.isDropdownOpen = !this.isDropdownOpen;
    },
    setLanguage(lang) {
      this.currentLanguage = lang;
      this.isDropdownOpen = false;
    }  }
}
</script>
