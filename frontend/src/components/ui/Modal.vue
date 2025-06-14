<template>
<div
    class="fixed inset-0 flex items-center justify-center
           bg-neutral-900/90 backdrop-blur-md">
    <div
      class="bg-neutral-900/90 backdrop-blur-md
             border border-neutral-700 text-gray-200
             p-6 rounded-lg shadow-lg w-full max-w-3xl">
      <slot/>
    </div>
  </div></template>

<script>
export default {
  name: 'Modal',
}
</script>
