<template>
  <div
    class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm"
  >
    <div
      class="bg-[#121212] border border-neutral-700 text-white p-6 rounded-xl shadow-xl w-full max-w-3xl"
    >
      <slot />
    </div>
  </div>
</template>


<script>
export default {
  name: "Modal",
};
</script>
