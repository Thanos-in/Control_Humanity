<template>
  <div>
    <h3 class="text-xl font-semibold mb-4 text-white">Новый проект</h3>

    <form
      @submit.prevent="handleSubmit"
      enctype="multipart/form-data"
      class="bg-[#121212] border border-neutral-700 text-white p-6 rounded-xl shadow-lg w-full max-w-3xl space-y-5"
    >
      <!-- Название проекта -->
      <div>
        <label class="block mb-1 font-medium text-sm text-gray-300" for="name">Название проекта *</label>
        <input
          v-model="form.name"
          id="name"
          type="text"
          placeholder="Введите название проекта"
          class="w-full p-2 rounded-lg border border-neutral-600 bg-neutral-900 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
          required
        />
      </div>

      <!-- Описание -->
      <div>
        <label class="block mb-1 font-medium text-sm text-gray-300" for="description">Описание</label>
        <textarea
          v-model="form.description"
          id="description"
          rows="3"
          placeholder="Введите описание проекта"
          class="w-full p-2 rounded-lg border border-neutral-600 bg-neutral-900 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
        ></textarea>
      </div>

      <!-- Менеджер -->
      <div>
        <label class="block mb-1 font-medium text-sm text-gray-300" for="manager">Назначить менеджера</label>
        <select
          v-model="form.manager_id"
          id="manager"
          class="w-full p-2 rounded-lg border border-neutral-600 bg-neutral-900 text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option disabled value="">Выберите менеджера</option>
          <option v-for="mgr in managers" :key="mgr.id" :value="mgr.id">
            {{ mgr.username }}
          </option>
        </select>
      </div>

      <!-- Дата окончания -->
      <div>
        <label class="block mb-1 font-medium text-sm text-gray-300" for="end_date">Дата окончания</label>
        <input
          v-model="form.end_date"
          id="end_date"
          type="date"
          class="w-full p-2 rounded-lg border border-neutral-600 bg-neutral-900 text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>

      <!-- Изображение проекта -->
      <div>
        <label class="block mb-1 font-medium text-sm text-gray-300" for="image">Изображение проекта</label>
        <input
          @change="handleImageChange"
          id="image"
          type="file"
          accept="image/*"
          class="w-full p-2 rounded-lg border border-neutral-600 bg-neutral-900 text-white file:mr-4 file:py-1 file:px-2 file:rounded file:border-0 file:text-sm file:font-semibold file:bg-blue-600 file:text-white hover:file:bg-blue-700"
        />
      </div>

      <!-- Ошибка -->
      <div v-if="errorMessage" class="text-red-400 text-sm">
        {{ errorMessage }}
      </div>

      <!-- Кнопки -->
      <div class="flex justify-end gap-3 pt-2">
        <button
          type="button"
          @click="$emit('cancel')"
          class="px-4 py-2 border border-gray-500 text-white rounded-md hover:bg-neutral-800 transition"
        >
          Отменить
        </button>
        <button
          type="submit"
          class="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-md transition"
          :disabled="loading"
        >
          <span v-if="loading">Добавление...</span>
          <span v-else>Добавить</span>
        </button>
      </div>
    </form>
  </div>
</template>


<script>
import api from "@/utils/axios";

export default {
  name: "ProjectForm",
  data() {
    return {
      form: {
        name: "",
        description: "",
        manager_id: "",
        end_date: "",
        image: null,
      },
      managers: [],
      loading: false,
      errorMessage: "",
    };
  },
  methods: {
    async fetchManagers() {
      try {
        const response = await api.get("/auth/users/managers/");
        this.managers = response.data;
      } catch (err) {
        console.error("Failed to fetch managers:", err);
      }
    },
    handleImageChange(event) {
      this.form.image = event.target.files[0];
    },
    async handleSubmit() {
      this.errorMessage = "";
      if (!this.form.name) {
        this.errorMessage = "Название проекта обязательно.";
        return;
      }

      const payload = new FormData();
      payload.append("name", this.form.name);
      payload.append("description", this.form.description);
      // payload.append('manager', this.form.manager)
      payload.append("manager_id", this.form.manager_id);
      if (this.form.end_date) payload.append("end_date", this.form.end_date);
      if (this.form.image) payload.append("image", this.form.image);

      try {
        this.loading = true;
        await api.post("/projects/", payload, {
          headers: { "Content-Type": "multipart/form-data" },
        });
        this.$emit("saved");
      } catch (err) {
        console.error(err);
        this.errorMessage = "Не удалось создать проект.";
      } finally {
        this.loading = false;
      }
    },
  },
  created() {
    this.fetchManagers();
  },
};
</script>
