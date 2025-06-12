<template>
  <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 p-4">
    <div v-if="loading" class="col-span-full text-center">Loading users...</div>
    <div v-if="error" class="col-span-full text-red-500 text-center">{{ error }}</div>

    

    <div
      v-for="user in users"
      :key="user.id"
      class="w-full max-w-sm bg-white border border-gray-200 rounded-lg shadow-sm dark:bg-gray-800 dark:border-gray-700"
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
              <button @click="editUser(user)" class="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 dark:hover:bg-gray-600 dark:text-gray-200 dark:hover:text-white">
                Edit
              </button>
            </li>
            <li>
              <button @click="exportUser(user)" class="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 dark:hover:bg-gray-600 dark:text-gray-200 dark:hover:text-white">
                Export Data
              </button>
            </li>
            <li>
              <button @click="deleteUser(user.id)" class="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-gray-100 dark:hover:bg-gray-600 dark:text-gray-200 dark:hover:text-white">
                Delete
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
            View Profile
          </button>
          <button
            @click="messageUser(user.id)"
            class="py-2 px-4 ms-2 text-sm font-medium text-gray-900 focus:outline-none bg-white rounded-lg border border-gray-200 hover:bg-gray-100 hover:text-blue-700 focus:z-10 focus:ring-4 focus:ring-gray-100 dark:focus:ring-gray-700 dark:bg-gray-800 dark:text-gray-400 dark:border-gray-600 dark:hover:text-white dark:hover:bg-gray-700"
          >
            Message
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
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
        const response = await axios.get('/api/auth/users/allusers/');
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

    const editUser = (user) => console.log('Edit', user);
    const exportUser = (user) => console.log('Export', user);
    const deleteUser = async (id) => {
      if (!confirm('Are you sure you want to delete this user?')) return;
      try {
        await axios.delete(`/api/auth/allusers/${id}/`);
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
      deleteUser,
      messageUser,
    };
  },
};
</script>

<style scoped>
/* Additional styling if needed */
</style>
