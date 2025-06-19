<template>
  <div class="flex-1 p-4 flex flex-col overflow-auto">
    <!-- Header -->
    <div class="flex items-center justify-between mb-6">
      <h2 class="text-3xl font-bold text-white">Проекты</h2>
      <button
        @click="showForm = true"
        class="bg-white text-purple-700 px-4 py-2 rounded-lg hover:bg-gray-100 shadow transition font-semibold text-sm"
      >
        + Новый проект
      </button>
    </div>

    <!-- Error -->
    <div
      v-if="projectError"
      class="mb-4 text-red-100 bg-red-500 p-3 rounded text-sm"
    >
      {{ projectError }}
    </div>

    <!-- Loading -->
    <div v-if="isLoading" class="flex-1 flex items-center justify-center">
      <span class="text-white opacity-90 text-lg">Загрузка проектов...</span>
    </div>

    <!-- List -->
    <ul v-else class="flex-1 overflow-auto space-y-4">
      <li
        v-for="proj in projects"
        :key="proj.id"
        class="bg-neutral-900/90 backdrop-blur-md border border-neutral-700 p-4 rounded-xl shadow hover:shadow-lg transition transform hover:scale-101 flex flex-col justify-between min-h-[160px] text-gray-200"
      >
        <div class="flex justify-between items-start">
          <router-link
            :to="`/projects/${proj.id}`"
            class="flex-1 pr-3 space-y-1"
          >
            <h3 class="text-xl font-semibold text-white-800">
              {{ proj.name }}
            </h3>
            <p class="text-gray-400 text-sm">{{ proj.description }}</p>
          </router-link>
          <!-- Delete Button -->
          <button
            @click="openDeleteInline(proj.id)"
            :disabled="deletingId === proj.id"
            class="text-red-600 hover:text-red-800 disabled:opacity-50"
          >
            <svg
              class="w-5 h-5"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </button>
        </div>
        <!-- Director / Manager -->
        <div class="mt-2 text-gray-400 text-xs">
          Директор: {{ proj.director.username }}
          <span v-if="proj.manager">
            | Менеджер: {{ proj.manager.username }}
          </span>
        </div>
      </li>
    </ul>

    <!-- Central Confirm Modal -->
    <div
      v-if="inlineDeleteId"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50"
    >
      <div
        class="bg-neutral-900/90 backdrop-blur-md border border-neutral-700 rounded-lg shadow p-6 w-80 text-gray-200"
      >
        <p class="text-sm mb-4">Вы действительно хотите удалить проект?</p>
        <div class="flex justify-end space-x-2">
          <button
            @click="cancelDelete"
            class="px-3 py-1 bg-gray-300 text-gray-800 rounded hover:bg-gray-400 text-xs"
          >
            Отменить
          </button>
          <button
            @click="confirmDelete"
            class="px-3 py-1 bg-red-500 text-white rounded hover:bg-red-600 text-xs"
          >
            Удалить
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- Modal: New Project -->
  <Modal v-if="showForm" @close="showForm = false">
    <ProjectForm @saved="onProjectSaved" @cancel="showForm = false" />
  </Modal>
</template>

<script>
import { mapGetters, mapActions, mapState } from "vuex";
import Modal from "../ui/Modal.vue";
import ProjectForm from "./ProjectForm.vue";

export default {
  name: "ProjectList",
  components: { Modal, ProjectForm },
  data() {
    return {
      showForm: false,
      deletingId: null,
      inlineDeleteId: null,
      projectIdToDelete: null,
    };
  },
  computed: {
    ...mapGetters("projects", ["allProjects", "isLoading", "projectError"]),
    ...mapState("auth", ["user"]), // ←– CHANGED: pull in current user
    projects() {
      // ←– CHANGED: filter by manager
      if (this.user.role === "director") {
        return this.allProjects;
      }
      return this.allProjects.filter(
        (proj) => proj.manager && proj.manager.id === this.user.id
      );
    },
  },
  methods: {
    ...mapActions("projects", ["fetchProjects", "deleteProject"]),
    onProjectSaved() {
      this.showForm = false;
      if (this.$route.path === "/projects") {
        this.$router.go(); 
      } else {
        this.$router.push("/projects");
      }
    },
    openDeleteInline(id) {
      this.inlineDeleteId = id;
      this.projectIdToDelete = id;
    },
    cancelDelete() {
      this.inlineDeleteId = null;
      this.projectIdToDelete = null;
    },
    async confirmDelete() {
      this.deletingId = this.projectIdToDelete;
      try {
        await this.deleteProject(this.projectIdToDelete);
      } catch (e) {
        console.error(e);
      } finally {
        this.deletingId = null;
        this.cancelDelete();
        this.fetchProjects();
      }
    },
  },
  created() {
    this.fetchProjects();
  },
};
</script>
