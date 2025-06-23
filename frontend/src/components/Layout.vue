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
          <!-- <div class="relative">
            <button
              @click.stop="toggleDropdown"
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
          </div> -->

          <div
            class="w-8 h-8 rounded-full overflow-hidden bg-gray-400 flex items-center dark:bg-gray-700"
          >
            <img
              @click.stop="userDropdown = !userDropdown"
              v-if="profile.profile_picture"
              :src="profile.profile_picture"
              alt="User Avatar"
              class="w-full h-full object-cover"
            />

            <div
              v-if="userDropdown"
              id="userDropdown"
              class="absolute right-0 top-full z-50 bg-white divide-y divide-gray-100 rounded-lg shadow-lg w-44 dark:bg-gray-700 dark:divide-gray-600"
            >
              <div class="px-4 py-3 text-sm text-gray-900 dark:text-white">
                <div>{{ profile.username }}</div>
                <div class="font-medium truncate">{{ profile.email }}</div>
              </div>
              <ul
                class="py-2 text-sm text-gray-700 dark:text-gray-200"
                aria-labelledby="avatarButton"
              >
                <li>
                  <button
                    type="button"
                    @click.stop="toggleProfileSettings"
                    class="flex items-center w-full p-2 text-base text-gray-900 transition duration-75 rounded-lg group hover:bg-gray-100 dark:text-white dark:hover:bg-gray-700"
                  >
                    <svg
                      class="w-3 h-3 text-gray-800 dark:text-white"
                      aria-hidden="true"
                      xmlns="http://www.w3.org/2000/svg"
                      fill="none"
                      viewBox="0 0 20 20"
                    >
                      <path
                        stroke="currentColor"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M4 12.25V1m0 11.25a2.25 2.25 0 0 0 0 4.5m0-4.5a2.25 2.25 0 0 1 0 4.5M4 19v-2.25m6-13.5V1m0 2.25a2.25 2.25 0 0 0 0 4.5m0-4.5a2.25 2.25 0 0 1 0 4.5M10 19V7.75m6 4.5V1m0 11.25a2.25 2.25 0 1 0 0 4.5 2.25 2.25 0 0 0 0-4.5ZM16 19v-2"
                      />
                    </svg>
                    <span
                      class="flex-1 ms-3 text-left rtl:text-right whitespace-nowrap"
                      >Settings</span
                    >
                    <svg
                      :class="[
                        'w-3 h-3 mr-2 transition-transform',
                        { 'rotate-180': profileSettings },
                      ]"
                      xmlns="http://www.w3.org/2000/svg"
                      fill="none"
                      viewBox="0 0 10 6"
                    >
                      <path
                        stroke="currentColor"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="m1 1 4 4 4-4"
                      />
                    </svg>
                  </button>
                  <ul
                    v-if="profileSettings"
                    id="dropdown-example"
                    class="py-2 space-y-2"
                  >
                    <li>
                      <router-link
                        v-if="$store.state.auth.token"
                        :to="`/profile/${$store.state.auth.user.id}`"
                      >
                        <span
                          class="block px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-600 rounded-lg dark:hover:text-white"
                        >
                          Profile
                        </span>
                      </router-link>
                    </li>
                    <li class="relative overflow-visible">
                      <button
                        @click.stop="toggleLanguage"
                        class="flex items-center w-full p-2 text-gray-900 dark:text-white hover:bg-gray-100 dark:hover:bg-gray-600 rounded-lg transition"
                      >
                        <!-- O‘q ikonkasi -->
                        <svg
                          :class="[
                            'w-3 h-3 mr-2 transition-transform',
                            { 'rotate-180': isLanguageOpen },
                          ]"
                          xmlns="http://www.w3.org/2000/svg"
                          fill="none"
                          viewBox="0 0 8 14"
                        >
                          <path
                            stroke="currentColor"
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            stroke-width="2"
                            d="M7 1 1.3 6.326a.91.91 0 0 0 0 1.348L7 13"
                          />
                        </svg>
                        Language
                      </button>

                      <!-- Yon tomonga chiqadigan submenu -->
                      <div
                        v-if="isLanguageOpen"
                        @click.stop
                        class="absolute top-1 right-[180px] mt-1 w-32 bg-white shadow-lg rounded p-2 z-50 dark:bg-gray-700"
                      >
                        <ul class="text-sm text-gray-900 dark:text-white">
                          <li v-for="lang in languages" :key="lang.code">
                            <a
                              href="#"
                              @click.prevent="setLanguage(lang.code)"
                              class="block px-2 py-1 rounded hover:bg-gray-200 dark:hover:bg-gray-600 transition"
                            >
                              {{ lang.label }}
                            </a>
                          </li>
                        </ul>
                      </div>
                    </li>
                    <li class="relative overflow-visible">
                      <button
                        @click.stop="toggleView"
                        class="flex items-center w-full p-2 text-gray-900 dark:text-white hover:bg-gray-100 dark:hover:bg-gray-600 rounded-lg transition"
                      >
                        <!-- O‘q ikonkasi -->
                        <svg
                          :class="[
                            'w-3 h-3 mr-2 transition-transform',
                            { 'rotate-180': isViewOpen },
                          ]"
                          xmlns="http://www.w3.org/2000/svg"
                          fill="none"
                          viewBox="0 0 8 14"
                        >
                          <path
                            stroke="currentColor"
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            stroke-width="2"
                            d="M7 1 1.3 6.326a.91.91 0 0 0 0 1.348L7 13"
                          />
                        </svg>
                        View
                      </button>

                      <div
                        v-if="isViewOpen"
                        @click.stop
                        class="absolute top-1 right-[180px] mt-1 w-32 bg-white shadow-lg rounded p-2 z-50 dark:bg-gray-700"
                      >
                        <ul class="text-sm text-gray-900 dark:text-white">
                          <li>
                            <a
                              href="#"
                              @click.prevent="setTheme('dark')"
                              :class="[
                                'px-2 py-1 rounded transition',
                                theme === 'dark'
                                  ? 'bg-gray-200 dark:bg-gray-600 font-semibold'
                                  : 'hover:bg-gray-200 dark:hover:bg-gray-600',
                              ]"
                            >
                              Dark
                            </a>

                            <a
                              href="#"
                              @click.prevent="setTheme('light')"
                              :class="[
                                'ml-2 px-2 py-1 rounded transition',
                                theme === 'light'
                                  ? 'bg-gray-200 dark:bg-gray-600 font-semibold'
                                  : 'hover:bg-gray-200 dark:hover:bg-gray-600',
                              ]"
                            >
                              Light
                            </a>
                          </li>
                        </ul>
                      </div>
                    </li>
                  </ul>
                </li>
                <li>
                  <a
                    href="#"
                    class="block px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-600 rounded-lg dark:hover:text-white"
                    >Earnings</a
                  >
                </li>
              </ul>
              <div class="py-1">
                <button
                  @click="showConfirmModal = true"
                  class="block w-full text-left px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-600 rounded-lg dark:hover:text-white"
                >
                  Log out
                </button>
              </div>
            </div>
          </div>
        </nav>
      </div>
    </header>

    <div class="flex flex-1 pt-[50px] overflow-hidden">
      <aside
        v-if="showSidebar"
        class="fixed top-[50px] left-0 h-[calc(100vh-50px)] w-56 bg-gray-300 border-r border-gray-400 shadow-inner z-40 px-3 py-5 text-gray-900 dark:bg-neutral-900/90 dark:border-neutral-700 dark:text-gray-200"
      >
        <nav class="flex flex-col space-y-2">
          <div
            v-if="$store.state.auth.user?.role !== 'employee'"
            class="relative"
          >
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

  <div
    v-if="showConfirmModal"
    class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50"
  >
    <div
      class="bg-neutral-900/90 backdrop-blur-md border border-neutral-700 rounded-lg shadow p-6 w-80 text-gray-200"
    >
      <p class="text-sm mb-4">Вы действительно хотите выйти из системы?</p>
      <div class="flex justify-end space-x-2">
        <button
          @click="cancelLogout"
          class="px-3 py-1 bg-gray-300 text-gray-800 rounded hover:bg-gray-400 text-xs"
        >
          Нет
        </button>

        <router-link
          to="/login"
          class="px-3 py-1 bg-red-500 text-white rounded hover:bg-red-600 text-xs"
        >
          Да
        </router-link>
      </div>
    </div>
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
      isLanguageOpen: false,
      showForm: false,
      userDropdown: false,
      isViewOpen: false,
      showConfirmModal: false,
      profileSettings: false,
      showProjectsDropdown: true,
      profileSettings: false,
      otherLinks: {
        tasks: "/mytasks",
        chat: "/chat",
        users: "/users",
        ratings: "/ratings",
      },
      error: null,
    };
  },
  methods: {
    setTheme(mode) {
      this.theme = mode;
      localStorage.setItem("theme", mode);
      if (mode === "dark") {
        document.documentElement.classList.add("dark");
      } else {
        document.documentElement.classList.remove("dark");
      }
    },
    toggleUserDropdown() {
      this.userDropdown = !this.userDropdown;
    },
    toggleLanguage() {
      this.isLanguageOpen = !this.isLanguageOpen;

      if (this.isLanguageOpen) {
        this.isViewOpen = false;
      }
    },
    toggleView() {
      this.isViewOpen = !this.isViewOpen;

      if (this.isViewOpen) {
        this.isLanguageOpen = false;
      }
    },
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
    toggleProfileSettings() {
      this.profileSettings = !this.profileSettings;

      if (!this.profileSettings) {
        this.isLanguageOpen = false;
        this.isViewOpen = false;
      }
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
    // projects aside
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
    cancelLogout() {
      this.showConfirmModal = false;
    },
    handleClickOutside(e) {
      if (!this.$el.contains(e.target)) {
        this.isDropdownOpen = false;
        this.userDropdown = false;

        if (!this.userDropdown) {
          this.profileSettings = false;
        }
        this.isLanguageOpen = false;
        this.profileSettings = false;
      }
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
  mounted() {
    document.documentElement.classList.add(this.theme);
    document.addEventListener("click", this.handleClickOutside);
  },
  beforeUnmount() {
    document.removeEventListener("click", this.handleClickOutside);
  },
};
</script>

<style>
/* Customize additional styles here */
</style>
