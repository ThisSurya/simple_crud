<script setup lang="ts">
// import { User } from "lucide-vue-next";

// modelValue otomatis di-handle oleh defineModel
const props = defineProps({
  modelValue: {
    type: String,
    default: "",
  },
  placeholder: {
    type: String,
    default: "Input...",
  },
  type: {
    type: String,
    default: "text",
  },
  icon: {
    type: Object, // Komponen ikon (User, Lock, Mail, dll.)
    default: null,
  },
  name: {
    type: String,
    default: "",
  },
});

const emit = defineEmits(["update:modelValue"]);
function onInput(event: Event) {
  const target = event.target as HTMLInputElement;
  emit("update:modelValue", target.value);
}
</script>

<template>
  <div class="rounded-md overflow-hidden border border-gray-300 bg-white w-full
           focus-within:ring-2 focus-within:ring-[#4A90E2]
           focus-within:border-[#4A90E2] flex items-center">
    <div v-if="icon" class="bg-[#f3e2d4]/50 flex items-center justify-center self-stretch px-2">
      <component :is="icon" class="w-5 h-5 stroke-[#17313E]" />
    </div>

    <input v-model="props.modelValue" @input="onInput" :type="props.type" :name="props.name"
      class="outline-none bg-transparent p-2 text-sm flex-1" :placeholder="props.placeholder" />
  </div>
</template>
