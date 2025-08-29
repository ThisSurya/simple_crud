<script setup lang="ts">
const props = defineProps({
  class: {
    type: String,
    default: ''
  }
});
</script>

<template>
  <div :class="['flex flex-col items-end justify-center space-y-2 bg-[#1F2937] self-stretch px-6', props.class]">
    <h1 class="text-2xl font-semibold text-white">Simple Dashboard</h1>
    <p class="text-white">By Vue 3, Vite and Tailwind CSS</p>
  </div>
</template>
