<template>
  <div
    class="h-screen flex flex-col bg-gray-200 dark:bg-gradient-to-br dark:from-[#692a88] dark:to-[#3b1555]"
  >
    <!-- Navbar -->
    <header
      class="fixed inset-x-0 top-0 z-50 bg-gray-300 dark:bg-gradient-to-r dark:from-[#3c0061] dark:to-[#1c002e] bg-opacity-90 backdrop-blur-md dark:bg-opacity-90"
    >
      <div class="grid grid-cols-[auto_1fr_auto] items-center px-4 py-3">
        <!-- Left -->
        <div class="flex items-center gap-3">
          <button
            @click="toggleSidebar"
            class="p-2 rounded bg-gray-400 hover:bg-gray-500 transition dark:bg-white/20 dark:hover:bg-white/30"
          >
            <svg
              class="w-5 h-5 text-gray-900 dark:text-white"
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
          <h1 class="text-xl font-semibold text-gray-900 dark:text-white">
            {{ $t("appTitle") }}
          </h1>
        </div>

        <!-- Center -->
        <div class="flex items-center justify-center space-x-2">
          <input
            type="text"
            :placeholder="$t('searchPlaceholder')"
            class="h-7 w-[700px] px-3 rounded-lg bg-gray-400 placeholder-gray-600 text-gray-900 text-sm focus:bg-gray-400 focus:outline-none transition dark:bg-gray-800 dark:placeholder-gray-400 dark:text-white"
          />
          <button
            @click="showForm = true"
            class="h-8 px-4 bg-gray-400 hover:bg-gray-500 text-gray-900 text-sm font-medium rounded-md shadow transition-colors duration-200 dark:bg-blue-700 dark:text-white dark:hover:bg-blue-800"
          >
            {{ $t("createButton") }}
          </button>
        </div>

        <!-- Right -->
        <nav class="flex items-center gap-3">
          <div class="relative">
            <button
              @click="toggleDropdown"
              class="flex items-center gap-1 px-3 py-1 text-xs text-gray-900 bg-gray-400 hover:bg-gray-500 rounded transition dark:bg-gradient-to-br dark:from-blue-500 dark:to-teal-400 dark:hover:from-blue-600 dark:hover:to-teal-500 dark:text-white"
            >
              {{ locale.toUpperCase() }}
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
              class="absolute right-0 mt-1 w-32 bg-white shadow rounded-sm z-10 dark:bg-neutral-900/90"
            >
              <ul class="text-xs text-gray-900 dark:text-white">
                <li v-for="lang in languages" :key="lang.code">
                  <a
                    href="#"
                    @click.prevent="setLanguage(lang.code)"
                    class="block px-3 py-1 rounded-sm hover:bg-gray-200 dark:hover:bg-gray-700"
                  >
                    {{ lang.label }}
                  </a>
                </li>
              </ul>
            </div>
          </div>

          <button
            @click="toggleTheme"
            class="px-3 py-1 text-xs rounded transition bg-gray-400 hover:bg-gray-500 text-gray-900 dark:bg-gray-600 dark:hover:bg-gray-500 dark:text-white"
          >
            {{ theme === "dark" ? "☀️" : "🌙" }}
          </button>

          <router-link
            v-if="$store.state.auth.token"
            :to="`/profile/${$store.state.auth.user.id}`"
          >
            <div
              class="w-8 h-8 rounded-full overflow-hidden bg-gray-400 flex items-center justify-center dark:bg-gray-700"
            >
              <img
                v-if="profile.profile_picture"
                :src="profile.profile_picture"
                alt="User Avatar"
                class="w-full h-full object-cover"
              />
              <span
                v-else
                class="text-gray-900 text-xs font-medium dark:text-white"
              >
                {{ getInitials(profile.username) }}
              </span>
            </div>
          </router-link>
        </nav>
      </div>
    </header>

    <div class="flex flex-1 pt-[50px] overflow-hidden">
      <aside
        v-if="showSidebar"
        class="fixed top-[50px] left-0 h-[calc(100vh-50px)] w-56 bg-gray-300 border-r border-gray-400 shadow-inner z-40 px-3 py-5 text-gray-900 dark:bg-neutral-900/90 dark:border-neutral-700 dark:text-gray-200"
      >
        <nav class="flex flex-col space-y-2">
          <div class="relative">
            <button
              @click="toggleProjects"
              class="flex items-center w-full px-2 py-1 text-sm font-medium text-gray-900 hover:text-gray-800 rounded transition dark:text-gray-300 dark:hover:text-white"
            >
              {{ $t("projects") }}
              <svg
                class="w-3 h-3 ml-auto text-gray-600 transition-transform duration-200 dark:text-gray-400"
                :class="{ 'rotate-180': showProjectsDropdown }"
                fill="none"
                viewBox="0 0 10 6"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
              >
                <path d="m1 1 4 4 4-4" />
              </svg>
            </button>
            <ul
              v-show="showProjectsDropdown"
              class="mt-1 space-y-1 bg-gray-200 rounded-md shadow-lg overflow-hidden dark:bg-gray-800"
            >
              <li>
                <router-link
                  to="/projects"
                  class="block px-4 py-2 text-sm text-gray-900 hover:bg-gray-300 dark:text-gray-300 dark:hover:bg-gray-700 dark:hover:text-white transition"
                >
                  {{ $t("allProjects") }}
                </router-link>
              </li>
              <li>
                <router-link
                  to="/archivedprojects"
                  class="block px-4 py-2 text-sm text-gray-900 hover:bg-gray-300 dark:text-gray-300 dark:hover:bg-gray-700 dark:hover:text-white transition"
                >
                  {{ $t("archived") }}
                </router-link>
              </li>
            </ul>
          </div>
          <router-link
            v-for="(path, key) in otherLinks"
            :key="key"
            :to="path"
            class="text-sm font-medium text-gray-900 hover:text-gray-800 px-2 py-1 rounded transition dark:text-gray-300 dark:hover:text-white"
          >
            {{ $t(key) }}
          </router-link>
        </nav>
      </aside>

      <main
        :class="[
          'flex-1 overflow-auto p-4 transition-all',
          showSidebar ? 'ml-56' : 'ml-0',
        ]"
      >
        <router-view />
      </main>
    </div>

    <Modal v-if="showForm" @close="showForm = false">
      <ProjectForm @saved="onProjectSaved" @cancel="showForm = false" />
    </Modal>
  </div>
</template>

<script>
import { useI18n } from "vue-i18n";
import api from "@/utils/axios";
import ProjectProgressChart from "@/components/ui/ProjectProgressChart.vue";
import Modal from "@/components/ui/Modal.vue";
import ProjectForm from "@/components/projects/ProjectForm.vue";

export default {
  name: "Layout",
  components: { ProjectProgressChart, ProjectForm, Modal },
  setup() {
    const { locale } = useI18n();
    const languages = [
      { code: "uz", label: "UZ" },
      { code: "ru", label: "RU" },
      { code: "en", label: "EN" },
    ];
    return { locale, languages };
  },
  data() {
    return {
      theme: localStorage.getItem("theme") || "dark",
      profile: {},
      showSidebar: true,
      isDropdownOpen: false,
      showForm: false,
      showProjectsDropdown: true,
      otherLinks: {
        tasks: "/mytasks",
        chat: "/chat",
        users: "/users",
        ratings: "/ratings",
      },
      error: null,
    };
  },
  mounted() {
    document.documentElement.classList.add(this.theme);
  },
  methods: {
    toggleTheme() {
      const newTheme = this.theme === "dark" ? "light" : "dark";
      this.theme = newTheme;
      localStorage.setItem("theme", newTheme);
      document.documentElement.classList.toggle("dark", newTheme === "dark");
    },
    toggleSidebar() {
      this.showSidebar = !this.showSidebar;
    },
    toggleDropdown() {
      this.isDropdownOpen = !this.isDropdownOpen;
    },
    async setLanguage(lang) {
      this.locale = lang;
      localStorage.setItem("lang", lang);
      this.isDropdownOpen = false;
      console.error("Ощибка!:", this.locale);
      try {
        await api.patch("/auth/users/me/", {
          language: lang,
        });
      } catch (err) {
        console.error("Ощибка!:", err);
      }
    },
    onProjectSaved() {
      this.showForm = false;
    },
    toggleProjects() {
      this.showProjectsDropdown = !this.showProjectsDropdown;
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
      const response = await api.get(`/auth/users/${id}/`);
      this.profile = response.data;

      if (this.profile.language) {
      this.locale = this.profile.language;
      localStorage.setItem("lang", this.profile.language);
      }
    } catch (e) {
      this.error = "Failed to load profile.";
      console.error(e);
    }
  },
};
</script>

<style>
/* Customize additional styles here */
</style>
