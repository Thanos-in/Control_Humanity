<template>
  <!-- ADD USER BUTTON -->
  <div class="flex justify-end p-4">
    <button
      @click="goToRegister"
      class="bg-white text-purple-700 px-6 py-3 rounded-lg hover:bg-gray-100 shadow-md hover:shadow-lg transition font-semibold text-lg"
    >
      + Добавить пользователя
    </button>
  </div>

  <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 p-4">
    <div v-if="loading" class="text-center">
      <div class="text-center ml-[510px]">
        <div role="status">
          <svg aria-hidden="true" class="inline w-10 h-10 text-gray-200 animate-spin dark:text-gray-600 fill-blue-600" viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z" fill="currentColor"/>
              <path d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z" fill="currentFill"/>
          </svg>
          <span class="sr-only">Loading...</span>
        </div>
      </div>
    </div>
    <div v-if="error" class="col-span-full text-red-500 text-center">{{ error }}</div>
    <div
      v-for="user in users"
      :key="user.id"
      class="w-full max-w-sm bg-white border border-gray-200 rounded-lg shadow-sm dark:bg-gray-800 dark:border-gray-700 background: linear-gradient(135deg, #3b4cca, #5b2c82)"
    >
      <div class="flex justify-end px-4 pt-4 relative">
        <button
          @click="toggleDropdown(user.id)"
          class="inline-block text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 focus:ring-4 focus:outline-none focus:ring-gray-200 dark:focus:ring-gray-700 rounded-lg text-sm p-1.5"
        >
          <span class="sr-only">Open dropdown</span>
          <svg class="w-5 h-5" aria-hidden="true" xmlns="www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 16 3">
            <path d="M2 0a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3Zm6.041 0a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3ZM14 0a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3Z"/>
          </svg>
        </button>
        <div
          v-show="dropdownOpen === user.id"
          @click.away="dropdownOpen = null"
          class="z-10 text-base list-none bg-white divide-y divide-gray-100 rounded-lg shadow-sm w-44 dark:bg-gray-700 absolute right-4 top-10"
        >
          <ul class="py-2">
            <li>
              <button @click="deleteUser(user.id)" class="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-gray-100 dark:hover:bg-gray-600 dark:text-gray-200 dark:hover:text-white">
                Удалить
              </button>
            </li>
          </ul>
        </div>
      </div>

      <div class="flex flex-col items-center pb-10">
        <img
          class="w-24 h-24 mb-3 rounded-full shadow-lg"
          :src="user.profile_picture || defaultAvatar"
          :alt="Avatar"/>

        <h5 class="mb-1 text-xl font-medium text-gray-900 dark:text-white">
          {{ user.full_name || user.username }}
        </h5>
        <span class="text-sm text-gray-500 dark:text-gray-400">
          {{ user.role || 'User' }}
        </span>
        <div class="flex mt-4 md:mt-6">
          <!-- Navigate to user profile by path -->
          <button
            @click="viewProfile(user.id)"
            class="inline-flex items-center px-4 py-2 text-sm font-medium text-center text-white bg-green-600 rounded-lg hover:bg-green-700 focus:ring-4 focus:outline-none focus:ring-green-300 dark:focus:ring-green-800"
          >
            Просматривать
          </button>
          <button
            @click="messageUser(user.id)"
            class="py-2 px-4 ms-2 text-sm font-medium text-gray-900 focus:outline-none bg-white rounded-lg border border-gray-200 hover:bg-gray-100 hover:text-blue-700 focus:z-10 focus:ring-4 focus:ring-gray-100 dark:focus:ring-gray-700 dark:bg-gray-800 dark:text-gray-400 dark:border-gray-600 dark:hover:text-white dark:hover:bg-gray-700"
          >
            Сообщение
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '@/utils/axios';
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import defaultAvatar from '../../assets/Default.png'

export default {
  name: 'UserList',
  setup() {
    const users = ref([]);
    const loading = ref(false);
    const error = ref(null);
    const dropdownOpen = ref(null);

    const router = useRouter();

    const fetchUsers = async () => {
      loading.value = true;
      try {
        const response = await api.get('/auth/users/');
        users.value = response.data;
      } catch (err) {
        error.value = 'Failed to load users.';
      } finally {
        loading.value = false;
      }
    };

    const toggleDropdown = (id) => {
      dropdownOpen.value = dropdownOpen.value === id ? null : id;
    };

    const viewProfile = (id) => {
      // push to /profile/:userId as configured in your router
      router.push({ path: `/profile/${id}` });
    };

    const goToRegister = () => {
      router.push('/register');
    };

    const editUser = (user) => console.log('Edit', user);
    const exportUser = (user) => console.log('Export', user);
    const deleteUser = async (id) => {
      if (!confirm('Are you sure you want to delete this user?')) return;
      try {
        await api.delete(`/auth/users/${id}/`);
        users.value = users.value.filter((u) => u.id !== id);
      } catch {
        alert('Delete failed.');
      }
    };
    const messageUser = (id) => console.log('Message', id);

    onMounted(fetchUsers);

    return {
      users,
      loading,
      error,
      dropdownOpen,
      toggleDropdown,
      viewProfile,
      defaultAvatar,
      editUser,
      exportUser,
      goToRegister,
      deleteUser,
      messageUser,
    };
  },
};
</script>
