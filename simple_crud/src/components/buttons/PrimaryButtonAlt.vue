<script setup lang="ts">
const props = defineProps<{
  type?: 'button' | 'submit' | 'reset'
  disabled?: boolean
  class?: string
}>()

const emit = defineEmits<{
  (e: 'click', event: MouseEvent): void
}>()
function handleClick(e: MouseEvent) {
  if (props.disabled) return
  emit('click', e)
}
</script>


<template>
  <button @click="handleClick" :type="props.type || 'button'" :disabled="props.disabled"
    :class="[' text-[#17313E] bg-white border-2 border-[#17313E] py-1.5 lg:px-4 md:px-4 px-2 text-sm rounded-md cursor-pointer hover:bg-[#17313E] hover:text-white duration-150 ease-in-out font-medium flex items-center justify-center', props.class]">
    <slot />
  </button>
</template>
