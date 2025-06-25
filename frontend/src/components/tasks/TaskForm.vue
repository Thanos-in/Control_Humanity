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
          <button
            v-if="
              localTask &&
              !localTask.is_archived &&
              localTask.assigned_to.id == $store.state.auth.user?.id
            "
            @click="toggleDone"
            type="button"
            class="text-white bg-gray-800 hover:bg-gray-900 focus:outline-none focus:ring-4 focus:ring-gray-300 font-medium rounded-lg text-sm px-5 py-2.5 me-2 mb-2 dark:bg-gray-800 dark:hover:bg-gray-700 dark:focus:ring-gray-700 dark:border-gray-700"
          >
            Done
          </button>
        </div>

        <!-- Если loadingTask, показываем загрузку -->
        <div v-if="loadingTask" class="text-gray-400">
          <div role="status">
            <svg
              aria-hidden="true"
              class="w-8 h-8 text-gray-200 animate-spin dark:text-gray-600 fill-blue-600"
              viewBox="0 0 100 101"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z"
                fill="currentColor"
              />
              <path
                d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z"
                fill="currentFill"
              />
            </svg>
            <span class="sr-only">Loading...</span>
          </div>
        </div>
        <!-- Если ошибка, можно здесь показать -->
        <div v-else-if="errorMessage" class="text-red-500">
          {{ errorMessage }}
        </div>
        <!-- Основной контент, когда localTask загружен -->
        <div v-else-if="localTask">
          <!-- SUB-HEADER: Title + Archive -->
          <div class="flex items-center space-x-3">
            <!-- Checkbox wrapper to apply peer -->
            <div
              v-if="$store.state.auth.user?.role !== 'employee'"
              class="relative flex items-center"
            >
              <!-- Checkbox input -->
              <input
                :id="`archive-cbx-${localTask.id}`"
                type="checkbox"
                :checked="localTask.is_archived"
                @change="onArchiveToggle"
                class="peer w-6 h-6 appearance-none border-2 border-gray-400 rounded-full transition-all duration-200 cursor-pointer hover:border-green-600 focus:outline-none"
              />

              <!-- Animatsion Label (splash) -->
              <label
                :for="`archive-cbx-${localTask.id}`"
                class="absolute inset-0 rounded-full pointer-events-none [filter:url(#goo)] peer-checked:animate-splash"
              ></label>

              <!-- Check icon -->
              <svg
                width="9"
                height="9"
                viewBox="0 0 15 14"
                fill="none"
                class="absolute inset-0 m-auto pointer-events-none"
              >
                <path
                  d="M2 8.36364L6.23077 12L13 2"
                  stroke="white"
                  stroke-width="3"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  class="stroke-dasharray-[19] stroke-dashoffset-[19] transition-all duration-500 peer-checked:stroke-dashoffset-0"
                />
              </svg>

              <!-- Gooey Filter (hidden) -->
              <svg
                xmlns="http://www.w3.org/2000/svg"
                version="1.1"
                class="hidden"
              >
                <defs>
                  <filter id="goo">
                    <feGaussianBlur
                      in="SourceGraphic"
                      stdDeviation="4"
                      result="blur"
                    />
                    <feColorMatrix
                      in="blur"
                      mode="matrix"
                      values="1 0 0 0 0  
                                0 1 0 0 0  
                                0 0 1 0 0  
                                0 0 0 22 -7"
                      result="goo"
                    />
                    <feBlend in="SourceGraphic" in2="goo" />
                  </filter>
                </defs>
              </svg>
            </div>

            <h3 class="ml-10 text-xl text-gray-200 font-medium">
              {{ localTask.title }}
            </h3>
          </div>

          <div class="mt-10 flex flex-wrap gap-4">
            <!-- METKI -->
            <div class="relative">
              <button
                @click.stop="toggleLabel"
                class="px-3 py-1.5 rounded text-sm text-gray-200 bg-[#2a2c2e] border border-gray-600 hover:bg-[#3a3b3e]"
              >
                Метка
              </button>
              <div
                v-if="showLabels"
                class="absolute w-[100px] mt-2 z-10 w-44 bg-[#1e1f22] border border-gray-600 rounded-lg shadow-lg"
                :style="{ backgroundColor: localTask?.color || '#1e1f22' }"
              >
                <ul class="py-2 text-sm text-gray-300">
                  <li>
                    <a
                      href="#"
                      class="block px-4 py-2 hover:bg-[#2a2c2e] hover:text-white"
                    ></a>
                  </li>
                </ul>
              </div>
            </div>

            <!-- DATY -->
            <div class="relative">
              <button
                @click.stop="toggleDueDate"
                class="px-3 py-1.5 rounded text-sm text-gray-200 bg-[#2a2c2e] border border-gray-600 hover:bg-[#3a3b3e]"
              >
                Даты
              </button>
              <div
                v-if="showDueDate"
                class="absolute w-[189px] mt-2 z-10 w-44 bg-[#1e1f22] border border-gray-600 rounded-lg shadow-lg"
              >
                <ul class="py-2 text-sm text-gray-300">
                  <li>
                    <a
                      href="#"
                      class="block px-4 py-2 hover:bg-[#2a2c2e] hover:text-white"
                    >{{ formatPeriod(localTask.created_at, localTask.due_date) }}</a>
                  </li>
                </ul>
              </div>
            </div>

            <!-- УЧАСТНИКИ -->
            <div class="relative">
              <button
                @click.stop="toggleMarkedted"
                class="px-3 py-1.5 rounded text-sm text-gray-200 bg-[#2a2c2e] border border-gray-600 hover:bg-[#3a3b3e]"
              >
                Участники
              </button>
              <div
                v-if="showParticipants"
                class="absolute top-full mt-2 z-10 w-44 bg-[#1e1f22] border border-gray-600 rounded-lg shadow-lg"
              >
                <ul class="py-2 text-sm text-gray-300">
                  <li v-for="user in localTask.marked_to" :key="user.id">
                    <a
                      href="#"
                      class="block px-4 py-2 hover:bg-[#2a2c2e] hover:text-white"
                    >
                      {{ user.username }}
                    </a>
                  </li>
                </ul>
              </div>
            </div>
          </div>


          <!-- Описание с форматированием -->
          <div>
            <h4 class="mt-10 flex items-center text-gray-400 mb-2">
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
                localTask.description ||
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
                ref="editorRef"
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
        <!-- Если localTask нет и нет loading, можно сообщить -->
        <div v-else class="text-gray-400">Задача не найдена</div>
      </div>

      <!-- RIGHT PANEL (1/3) -->
      <div
        v-if="localTask"
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
                <span class="font-semibold text-white">
                  {{ localTask.first_name + " " + localTask.last_name }}
                </span>
                добавил(а) эту карточку в список {{ localTask.title }}
              </p>
              <p class="text-gray-500 text-xs mt-1">
                {{ formatDate(localTask.data_input) }}
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
    <div
      id="toast-undo"
      v-show="showToast"
      class="fixed bottom-4 right-4 flex items-center w-full max-w-xs p-4 text-gray-500 bg-white rounded-lg shadow-sm dark:text-gray-400 dark:bg-gray-800 z-50"
      role="alert"
    >
      <div class="text-sm font-normal">{{ toastMessage }}</div>
      <div class="flex items-center ms-auto space-x-2 rtl:space-x-reverse">
        <!-- <button
      @click="undoArchive"
      class="text-sm font-medium text-blue-600 p-1.5 hover:bg-blue-100 rounded-lg dark:text-blue-500 dark:hover:bg-gray-700"
    >
      Undo
    </button> -->
        <button
          @click="showToast = false"
          class="ms-auto -mx-1.5 -my-1.5 bg-white text-gray-400 hover:text-gray-900 rounded-lg focus:ring-2 focus:ring-gray-300 p-1.5 hover:bg-gray-100 inline-flex items-center justify-center h-8 w-8 dark:text-gray-500 dark:hover:text-white dark:bg-gray-800 dark:hover:bg-gray-700"
        >
          <svg
            class="w-3 h-3"
            aria-hidden="true"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 14 14"
          >
            <path
              stroke="currentColor"
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6"
            />
          </svg>
        </button>
      </div>
    </div>
  </div>
  <div
    v-if="showConfirmModal"
    class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50"
  >
    <div
      class="bg-neutral-900/90 backdrop-blur-md border border-neutral-700 rounded-lg shadow p-6 w-80 text-gray-200"
    >
      <p class="text-sm mb-4">
        Вы согласны с тем, что задача переходит к другому человеку
      </p>
      <div class="flex justify-end space-x-2">
        <button
          @click="cancelDone"
          class="px-3 py-1 bg-gray-300 text-gray-800 rounded hover:bg-gray-400 text-xs"
        >
          Нет
        </button>
        <button
          @click="confirmDone"
          class="px-3 py-1 bg-red-500 text-white rounded hover:bg-red-600 text-xs"
        >
          Да
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useStore } from "vuex";
import { ref, onMounted, nextTick, watch, computed, onBeforeUnmount } from "vue";
import { useRoute, useRouter } from "vue-router";
import api from "@/utils/axios";

const route = useRoute();
const store = useStore();
const router = useRouter();
const taskId = route.params.taskId;

// Если parent передает props.task, опционально:
const props = defineProps({
  task: {
    type: Object,
    required: false,
  },
});
const emit = defineEmits(["update:task", "close"]);

// State
const localTask = ref(null);
const loadingTask = ref(false);
const loadingArchive = ref(false);
const errorMessage = ref("");
const showToast = ref(false);
const toastMessage = ref("");
const showLabels = ref(false)
const showParticipants = ref(false)
const showDueDate = ref(false)

// Description editing
const editingDesc = ref(false);
const editedHtml = ref("");
const editorRef = ref(null);
const showConfirmModal = ref(false);

// Определяем, из архива или нет через query
const isArchivedContext = computed(() => route.query.archived !== undefined);

function showArchiveToast(archived) {
  toastMessage.value = archived
    ? "Задача отправлена в архив."
    : "Задача восстановлена из архива.";
  showToast.value = true;
  setTimeout(() => (showToast.value = false), 5000);
}
function toggleDone() {
  showConfirmModal.value = true;
}
function cancelDone() {
  showConfirmModal.value = false;
}

function formatPeriod(createdAt, dueDate) {
  const from = formatDate(createdAt);
  const to = dueDate ? formatDate(dueDate) : "-";
  return `${from} → ${to}`;
}

function confirmDone() {
  if (!localTask.value) return;

  api
    .patch(`/tasks/${localTask.value.id}/`, { done: true })
    .then((res) => {
      localTask.value = res.data;
      showConfirmModal.value = false;
      toastMessage.value = "Topshiriq keyingisiga o'tdi.";
      showToast.value = true;
      setTimeout(() => (showToast.value = false), 5000);
      emit("update:task", res.data);
    })
    .catch((err) => {
      console.error("Xatolik:", err);
      showConfirmModal.value = false;
      alert("Topshiriqni yakunlashda xatolik.");
    });
  showConfirmModal.value = false;
}

// Если передан props.task, инициализируем localTask:
if (props.task) {
  localTask.value = { ...props.task };
}
// Следим за изменением props.task:
watch(
  () => props.task,
  (newTask) => {
    if (newTask) {
      localTask.value = { ...newTask };
    }
  }
);

// Если route.query.archived меняется и нет props.task, повторно загрузить:
watch(
  () => route.query.archived,
  () => {
    if (!props.task) {
      fetchTask();
    }
  }
);

function fetchTask() {
  if (!taskId) {
    console.warn("taskId не задан");
    return;
  }
  loadingTask.value = true;
  errorMessage.value = "";
  const url = `/tasks/${taskId}/`;
  const params = { is_archived: isArchivedContext.value ? "true" : "false" };
  if (isArchivedContext.value) {
    params.is_archived = "true";
  }
  api
    .get(url, { params })
    .then((res) => {
      localTask.value = res.data;
      emit("update:task", res.data);
    })
    .catch((err) => {
      console.error("Task yuklanmadi:", err);
      if (err.response?.status === 404 && isArchivedContext.value) {
        errorMessage.value =
          "Архивированная задача не найдена или доступ запрещён";
      } else {
        errorMessage.value = "Ошибка при загрузке задачи";
      }
    })
    .finally(() => {
      loadingTask.value = false;
    });
}

function onArchiveToggle(event) {
  if (!localTask.value) return;
  const newState = event.target.checked;
  loadingArchive.value = true;
  api
    .patch(`/tasks/${localTask.value.id}/archive/`, { is_archived: newState })
    .then((res) => {
      localTask.value = { ...res.data };
      emit("update:task", res.data);

      showArchiveToast(newState);
    })
    .catch((err) => {
      console.error("Archive toggle error:", err);
      if (localTask.value) {
        localTask.value.is_archived = !newState;
      }
      if (err.response?.status === 403) {
        alert("У вас нет прав для архивирования этой задачи.");
      } else {
        alert("Ошибка при изменении статуса архивации. Повторите попытку.");
      }
    })
    .finally(() => {
      loadingArchive.value = false;
    });
}

function startEditingDesc() {
  if (store.state.auth.user?.role !== "employee") {
    if (!localTask.value) return;
    editingDesc.value = true;
    editedHtml.value = localTask.value.description || "";
    nextTick(() => {
      if (editorRef.value) {
        editorRef.value.innerHTML = editedHtml.value;
      }
    });
  }
}

function cancelDescription() {
  editingDesc.value = false;
}

function submitEdit() {
  if (!localTask.value) return;
  const payload = {
    title: localTask.value.title,
    project_id: localTask.value.project_id,
    status_id: localTask.value.status_id,
  };
  if (editingDesc.value && editorRef.value) {
    payload.description = editorRef.value.innerHTML;
  }
  api
    .put(`/tasks/${taskId}/`, payload)
    .then((res) => {
      localTask.value = res.data;
      editingDesc.value = false;
      alert("Описание успешно обновлено");
      emit("update:task", res.data);
    })
    .catch((err) => {
      console.error("Xatolik:", err);
      alert(
        "Ошибка при сохранении описания: " +
          (err.response?.data?.detail || JSON.stringify(err.response?.data))
      );
    });
}

function format(cmd) {
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

function formatDate(d) {
  if (!d) return "Noma’lum";
  return new Date(d).toLocaleDateString();
}

function closeModal() {
  router.back();
  emit("close");
}

function toggleLabel() {
  showLabels.value = !showLabels.value
  if (showLabels.value) {
    showParticipants.value = false
    showDueDate.value = false
  }
}

function toggleMarkedted() {
  showParticipants.value = !showParticipants.value
  if (showParticipants.value) {
    showLabels.value = false
    showDueDate.value = false
  }
}

function toggleDueDate() {
  showDueDate.value = !showDueDate.value
  if (showDueDate.value) {
    showLabels.value = false
    showParticipants.value = false
  }
}

const closeAllDropdowns = () => {
  showLabels.value = false
  showDueDate.value = false
  showParticipants.value = false
}

const handleClickOutside = (event) => {
  if (!event.target.closest('.dropdown-wrapper')) {
    closeAllDropdowns()
  }
}

onMounted(() => {
  if (!props.task) {
    fetchTask();
  }
  window.addEventListener('click', handleClickOutside)  
});
onBeforeUnmount(() => {
  window.removeEventListener('click', handleClickOutside)
});
</script>

<style scoped>
/* Добавьте дополнительные стили, если нужно */
</style>
