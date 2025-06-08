<template>
  <div class="fixed inset-0 flex items-center justify-center bg-gray-800 bg-opacity-50">
    <div class="bg-white p-6 rounded-lg shadow-lg w-full max-w-3xl">
      <slot/>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Modal',
}
</script>
