<template>
  <div
    class="h-screen flex flex-col bg-gradient-to-br from-indigo-500 via-purple-600 to-pink-500"
  >
    <!-- Navbar -->
    <header
      class="fixed inset-x-0 top-0 z-50 bg-gradient-to-r from-purple-700 to-indigo-600 bg-opacity-90 backdrop-blur-md border-b"
    >
      <div class="flex items-center justify-between px-4 py-3">
        <!-- Left -->
        <div class="flex items-center gap-3">
          <button
            @click="toggleSidebar"
            class="p-2 rounded bg-white/20 hover:bg-white/30 transition"
          >
            <svg
              class="w-5 h-5 text-white"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M4 6h16M4 12h16M4 18h16"
              />
            </svg>
          </button>
          <h1 class="text-xl font-semibold text-white">All Personal Soft</h1>
        </div>

        <!-- Right -->
        <nav class="relative flex items-center gap-3">
          <router-link
            v-for="(label, path) in navLinks"
            :key="path"
            :to="path"
            class="text-sm text-white hover:text-yellow-200 transition px-2 py-1"
          >
            {{ label }}
          </router-link>

          <!-- Language -->
          <div class="relative">
            <button
              @click="toggleDropdown"
              class="flex items-center gap-1 px-3 py-1 text-xs text-white bg-gradient-to-br from-blue-500 to-teal-400 hover:from-blue-600 hover:to-teal-500 rounded transition"
            >
              {{ currentLanguage }}
              <svg class="w-3 h-3" fill="none" viewBox="0 0 10 6">
                <path
                  stroke="currentColor"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="m1 1 4 4 4-4"
                />
              </svg>
            </button>
            <div
              v-show="isDropdownOpen"
              class="absolute right-0 mt-1 w-32 bg-white/90 backdrop-blur-md shadow rounded z-10"
            >
              <ul class="text-xs text-gray-800">
                <li>
                  <a
                    href="#"
                    @click.prevent="setLanguage('Eng')"
                    class="block px-3 py-1 hover:bg-gray-100"
                    >Eng</a
                  >
                </li>
                <li>
                  <a
                    href="#"
                    @click.prevent="setLanguage('Ru')"
                    class="block px-3 py-1 hover:bg-gray-100"
                    >Ru</a
                  >
                </li>
              </ul>
            </div>
          </div>

          <!-- Profile -->
          <router-link
            v-if="$store.state.auth.token"
            :to="`/profile/${$store.state.auth.user.id}`"
          >
            <div
              class="w-8 h-8 rounded-full overflow-hidden bg-white/40 flex items-center justify-center"
            >
              <!-- Agar rasm bo'lsa -->
              <img
                v-if="profile.profile_picture"
                :src="profile.profile_picture"
                alt="User Avatar"
                class="w-full h-full object-cover"
              />
              <!-- Rasm bo'lmasa, initials -->
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
        "/tasks": "Задачи",
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
