<template>
  <div
    class="h-screen flex flex-col bg-gradient-to-br from-[#692a88] to-[#3b1555]"
  >
    <!-- Navbar -->
<header
  class="fixed inset-x-0 top-0 z-50 bg-gradient-to-r from-[#3c0061] to-[#1c002e] bg-opacity-90 backdrop-blur-md"
>
  <!-- 3 ustunli grid: chap auto, o'rta 1fr, o'ng auto -->
  <div class="grid grid-cols-[auto_1fr_auto] items-center px-4 py-3">
    <!-- Left -->
    <div class="flex items-center gap-3">
      <button
        @click="toggleSidebar"
        class="p-2 rounded bg-white/20 hover:bg-white/30 transition"
      >
        <!-- ikonka -->
        <svg
          class="w-5 h-5 text-white"
          fill="none" viewBox="0 0 24 24" stroke="currentColor"
        >
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
            d="M4 6h16M4 12h16M4 18h16"
          />
        </svg>
      </button>
      <h1 class="text-xl font-semibold text-white">All Personal Soft</h1>
    </div>

    <!-- Center: Search -->
    <div class="flex items-center justify-center space-x-2">
      <input
        type="text"
        placeholder="Поиск..."
        class="h-7 w-[700px] px-3 rounded-lg bg-white/20 placeholder-white text-white text-sm focus:bg-white/30 focus:outline-none transition"
      />
      <button
        class="h-8 px-4 bg-blue-500 hover:bg-blue-600 text-black text-sm font-medium rounded-md shadow transition-colors duration-200"
      >
        Создать
      </button>
    </div>


    <!-- Right -->
    <nav class="flex items-center gap-3">
      <!-- til tanlash -->
      <div class="relative">
        <button
          @click="toggleDropdown"
          class="flex items-center gap-1 px-3 py-1 text-xs text-white bg-gradient-to-br from-blue-500 to-teal-400 hover:from-blue-600 hover:to-teal-500 rounded transition"
        >
          {{ currentLanguage }}
          <svg class="w-3 h-3" fill="none" viewBox="0 0 10 6">
            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="m1 1 4 4 4-4"
            />
          </svg>
        </button>
        <div
          v-show="isDropdownOpen"
          class="absolute right-0 mt-1 w-32 bg-neutral-900/90 shadow rounded-sm z-10"
        >
          <ul class="text-xs text-gray-800">
            <li>
              <a href="#" @click.prevent="setLanguage('Eng')"
                class="block px-3 py-1 rounded-sm text-white hover:bg-gray-700"
                >Eng</a
              >
            </li>
            <li>
              <a href="#" @click.prevent="setLanguage('Ru')"
                class="block px-3 py-1 rounded-sm text-white hover:bg-gray-700"
                >Ru</a
              >
            </li>
          </ul>
        </div>
      </div>

      <!-- profil -->
      <router-link
        v-if="$store.state.auth.token"
        :to="`/profile/${$store.state.auth.user.id}`"
      >
        <div
          class="w-8 h-8 rounded-full overflow-hidden bg-white/40 flex items-center justify-center"
        >
          <img
            v-if="profile.profile_picture"
            :src="profile.profile_picture"
            alt="User Avatar"
            class="w-full h-full object-cover"
          />
          <span v-else class="text-white text-xs font-medium">
            {{ getInitials(profile.username) }}
          </span>
        </div>
      </router-link>
    </nav>
  </div>
</header>

    <!-- Layout -->
    <div class="flex flex-1 pt-[50px] overflow-hidden">
      <!-- Sidebar -->
      <aside
        v-if="showSidebar"
        class="fixed top-[50px] left-0 h-[calc(100vh-50px)] w-56 bg-neutral-900/90 backdrop-blur-md border-r border-neutral-700 shadow-inner z-40 px-3 py-5 text-gray-200"
      >
        <nav class="flex flex-col space-y-2">
          <router-link
            v-for="(label, path) in navLinks"
            :key="path"
            :to="path"
            class="text-sm font-medium text-gray-300 hover:text-white px-2 py-1 rounded transition"
            active-class="bg-neutral-800 text-white"
          >
            {{ label }}
          </router-link>
        </nav>
      </aside>

      <!-- Content -->
      <main
        :class="[
          'flex-1 overflow-auto p-4 transition-all',
          showSidebar ? 'ml-56' : 'ml-0',
        ]"
      >
        <router-view />
      </main>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "Layout",
  data() {
    return {
      profile: {},
      showSidebar: true,
      isDropdownOpen: false,
      currentLanguage: "Ru",
      navLinks: {
        "/projects": "Проекты",
        "/mytasks": "Задачи",
        "/chat": "Чаты",
        "/users": "Пользователи",
        "/ratings": "Рейтинг",
      },
      error: null,
    };
  },
  methods: {
    toggleSidebar() {
      this.showSidebar = !this.showSidebar;
    },
    toggleDropdown() {
      this.isDropdownOpen = !this.isDropdownOpen;
    },
    setLanguage(lang) {
      this.currentLanguage = lang;
      this.isDropdownOpen = false;
    },
    getInitials(name) {
      if (!name) return "";
      return name
        .split(" ")
        .map((n) => n.charAt(0).toUpperCase())
        .join("");
    },
  },

  async created() {
    try {
      const id = this.$store.state.auth.user.id;
      const response = await axios.get(`/api/auth/profiles/${id}/`);
      this.profile = response.data;
    } catch (e) {
      this.error = "Failed to load profile.";
      console.error(e);
    }
  },
};
</script>
