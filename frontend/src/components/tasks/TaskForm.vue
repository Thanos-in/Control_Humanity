<template>
  <!-- Modal Overlay -->
  <div
    class="mt-50 fixed inset-0 bg-black bg-opacity-60 flex items-start justify-center pt-16 px-4 z-50"
  >
    <!-- Modal Container -->
    <div
      class="bg-[#1e1f22] w-full max-w-6xl rounded-xl shadow-2xl max-h-[90vh] overflow-y-auto flex relative"
    >
      <!-- LEFT PANEL (2/3) -->
      <div class="w-2/3 p-6 space-y-6">
        <!-- HEADER: Title -->
        <div class="flex items-center justify-between mb-8">
          <h2 class="text-4xl font-bold text-gray-200">Детали задачи</h2>
        </div>

        <!-- SUB-HEADER: Title -->
        <div class="flex items-center space-x-3">
          <div class="flex items-center mb-4">
            <input
              id="default-checkbox"
              type="checkbox"
              value=""
              class="mt-5 w-4 h-4 text-green-600 bg-green-100 border-green-300 rounded-full focus:ring-green-500 dark:focus:ring-green-600 dark:ring-offset-green-800 focus:ring-2 dark:bg-green-700 dark:border-green-600"
            />
            <label
              for="default-checkbox"
              class="ms-2 text-sm font-medium rounded-full text-green-900 dark:text-green-300"
              ></label
            >
          </div>
          <h3 class="text-xl text-gray-200 font-medium">{{ task.title }}</h3>
        </div>

        <!-- Buttons -->
        <div class="flex flex-wrap gap-2">
          <button
            class="px-3 py-1.5 border border-gray-600 rounded text-sm text-gray-300 hover:bg-gray-700"
          >
            + Добавить
          </button>
          <button
            class="px-3 py-1.5 border border-gray-600 rounded text-sm text-gray-300 hover:bg-gray-700"
          >
            Метки
          </button>
          <button
            class="px-3 py-1.5 border border-gray-600 rounded text-sm text-gray-300 hover:bg-gray-700"
          >
            Даты
          </button>
          <button
            class="px-3 py-1.5 border border-gray-600 rounded text-sm text-gray-300 hover:bg-gray-700"
          >
            Чек‑лист
          </button>
          <button
            class="px-3 py-1.5 border border-gray-600 rounded text-sm text-gray-300 hover:bg-gray-700"
          >
            Участники
          </button>
        </div>

        <!-- Описание с форматированием -->
        <div>
          <h4 class="flex items-center text-gray-400 mb-2">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-5 w-5 mr-1"
              viewBox="0 0 20 20"
              fill="currentColor"
            >
              <path
                fill-rule="evenodd"
                d="M5 4a1 1 0 011-1h8a1 1 0 011 1v1H5V4zm0 3h10v9a1 1 0 01-1 1H6a1 1 0 01-1-1V7z"
                clip-rule="evenodd"
              />
            </svg>
            Описание
          </h4>

          <!-- Просмотр -->
          <div
            v-if="!editingDesc"
            @click="startEditingDesc"
            class="cursor-pointer bg-[#2a2c2e] border border-gray-600 rounded px-3 py-2 text-sm text-gray-300 whitespace-pre-wrap"
            v-html="
              task.description ||
              '<i class=text-gray-500>Добавить описание...</i>'
            "
          ></div>

          <!-- Редактирование -->
          <div v-else class="space-y-3">
            <!-- Панель форматирования -->
            <div class="flex flex-wrap gap-2 mb-1">
              <button
                @click.prevent="format('bold')"
                title="Жирный"
                class="px-2 py-1 border border-gray-600 rounded text-sm text-gray-300 hover:bg-gray-700"
              >
                B
              </button>
              <button
                @click.prevent="format('italic')"
                title="Курсив"
                class="px-2 py-1 border border-gray-600 rounded text-sm text-gray-300 hover:bg-gray-700"
              >
                <i>I</i>
              </button>
              <button
                @click.prevent="format('h1')"
                title="Заголовок 1"
                class="px-2 py-1 border border-gray-600 rounded text-sm text-gray-300 hover:bg-gray-700"
              >
                H1
              </button>
              <button
                @click.prevent="format('h2')"
                title="Заголовок 2"
                class="px-2 py-1 border border-gray-600 rounded text-sm text-gray-300 hover:bg-gray-700"
              >
                H2
              </button>
              <button
                @click.prevent="format('small')"
                title="Мелкий текст"
                class="px-2 py-1 border border-gray-600 rounded text-sm text-gray-300 hover:bg-gray-700"
              >
                small
              </button>
              <button
                @click.prevent="format('big')"
                title="Большой текст"
                class="px-2 py-1 border border-gray-600 rounded text-sm text-gray-300 hover:bg-gray-700"
              >
                big
              </button>
            </div>
            <!-- Редактируемый блок -->
            <div
              ref="editor"
              contenteditable="true"
              class="min-h-[100px] w-full bg-[#2a2c2e] border border-gray-600 rounded px-3 py-2 text-sm text-gray-300 placeholder-gray-500 focus:outline-none overflow-auto"
            >
              {{ editedHtml }}
            </div>

            <!-- Сохранить / Отмена -->
            <div class="flex space-x-2">
              <button
                type="submit"
                @click.prevent="submitEdit"
                class="bg-blue-600 hover:bg-blue-700 px-5 py-2 rounded text-sm font-medium text-black"
              >
                Сохранить
              </button>
              <button
                type="button"
                @click.prevent="cancelDescription"
                class="px-5 py-2 rounded text-sm text-gray-400 hover:text-gray-200"
              >
                Отмена
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- RIGHT PANEL (1/3) -->
      <div
        class="w-1/3 bg-[#242629] border-l border-gray-700 p-6 flex flex-col"
      >
        <h4 class="text-gray-300 font-semibold mb-4">Комментарии и события</h4>
        <textarea
          rows="2"
          class="w-full bg-[#1e1f22] border border-gray-600 rounded px-3 py-2 text-sm text-gray-300 placeholder-gray-500 focus:outline-none resize-none mb-3"
          placeholder="Напишите комментарий..."
        ></textarea>
        <button
          class="self-end bg-blue-600 hover:bg-blue-700 px-4 py-1.5 rounded mb-4 text-sm font-medium text-black"
        >
          Отправить
        </button>

        <div class="overflow-y-auto flex-1 space-y-4">
          <div class="flex items-start space-x-3">
            <div
              class="w-8 h-8 flex-shrink-0 flex-grow-0 rounded-full bg-white border border-white"
            ></div>
            <div>
              <p class="text-gray-200 text-sm">
                <span class="font-semibold text-white"
                  >{{ task.first_name + " " + task.last_name }}
                </span>
                добавил(а) эту карточку в список {{ task.title }}
              </p>
              <p class="text-gray-500 text-xs mt-1">
                {{ formatDate(task.data_input) }}
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- Close Modal Button -->
      <button
        @click="closeModal"
        class="absolute top-4 right-4 text-gray-400 hover:text-gray-200"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="h-6 w-6"
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
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from "vue";
import { useRoute, useRouter } from "vue-router";
import axios from "axios";

const route = useRoute();
const router = useRouter();
const taskId = route.params.taskId;

const task = ref({
  title: "",
  description: "",
  first_name: "",
  last_name: "",
  data_input: "",
});
const editingDesc = ref(false);
const editedHtml = ref("");

// Загрузка задачи
function fetchTask() {
  axios
    .get(`/api/tasks/${taskId}/`)
    .then((res) => {
      task.value = res.data;
    })
    .catch((err) => console.error("Task yuklanmadi:", err));
}

// Форматирование через execCommand
function format(cmd) {
  let value;
  switch (cmd) {
    case "h1":
      document.execCommand("formatBlock", false, "<h1>");
      return;
    case "h2":
      document.execCommand("formatBlock", false, "<h2>");
      return;
    case "small":
      document.execCommand("fontSize", false, "1");
      return;
    case "big":
      document.execCommand("fontSize", false, "4");
      return;
    default:
      document.execCommand(cmd);
  }
}

// Начать редактирование
function startEditingDesc() {
  editingDesc.value = true;
  editedHtml.value = task.value.description || "";
  nextTick(() => {
    // Устанавливаем содержимое
    editorRef.value.innerHTML = editedHtml.value;
  });
}

// Отмена редактирования
function cancelDescription() {
  editingDesc.value = false;
}

// Сохранение описания
function submitEdit() {
  const payload = {
    title: task.value.title,
    description: editorRef.value,
    project_id: task.value.project_id,
    status_id: task.value.status_id,
  };
  console.log("Yuborilayotgan payload:", payload);

  // Faqat description tahrirlanayotgan bo‘lsa, uni yangilash
  if (editingDesc.value && editorRef.value) {
    payload.description = editorRef.value.innerHTML;
  } else {
    // Bu holatda description umuman yuborilmaydi
    delete payload.description;
  }

  axios
    .put(`/api/tasks/${taskId}/`, payload)
    .then((res) => {
      console.table(res.data);
      task.value = res.data;
      editingDesc.value = false;
      alert("Описание успешно обновлено");
    })
    .catch((err) => {
      console.error("Xatolik:", err);
      alert(
        "Xatolik yuz berdi: " +
          (err.response?.data?.detail || JSON.stringify(err.response?.data))
      );
    });
}

// Утилиты
function formatDate(d) {
  if (!d) return "Noma’lum";
  return new Date(d).toLocaleDateString();
}

function closeModal() {
  router.back();
}

const editorRef = ref(null);

onMounted(fetchTask);
</script>

<style scoped>
/* Можно добавить дополнительные стили для заголовков внутри contenteditable */
</style>
