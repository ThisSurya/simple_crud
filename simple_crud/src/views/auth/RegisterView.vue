<script setup lang="ts">
// import
import PrimaryButton from '@/components/buttons/PrimaryButton.vue';
import InputField from '@/components/InputField.vue';
import { RequestHttp } from '@/util/Request';
import { IdCard, KeySquare, Mail, User } from 'lucide-vue-next';
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

const username = ref('');
const password = ref('');
const name = ref('');
const email = ref('');
const error = ref('');
const success = ref('');

function validate() {
  if (username.value === '' || password.value.length < 8 || name.value === '' || email.value === '') {
    error.value = 'All fields are required, password must be at least 8 characters';
    return false;
  }
  return true;
}

async function OnSubmit(e: Event) {
  e.preventDefault();
  error.value = '';
  if (!validate()) return;

  const result = await RequestHttp({
    type: 'post',
    url: `/register`,
    datas: {
      username: username.value,
      password: password.value,
      name: name.value,
      email: email.value,
    }
  });

  if (result.status === 'failed') {
    error.value = result.message || 'Registration failed';
    return;
  }

  success.value = 'Registration successful! Redirecting to login...';
  username.value = '';
  password.value = '';
  name.value = '';
  email.value = '';
  router.push('/');
}
</script>

<template>
  <section class="bg-white rounded-xl gap-x-4 flex items-center justify-center m-auto overflow-hidden min-h-[325px]">
    <div class="flex flex-col p-4 px-6 gap-y-7 w-[350px]">
      <div class="space-y-2">
        <h1 class="text-2xl font-semibold text-[#1F2937] text-center">Simple Dashboard</h1>
        <p class="text-xs text-[#1F2937]/75 text-center">Register page</p>
      </div>
      <form @submit="OnSubmit" class="space-y-3">
        <InputField v-model="username" name="username" placeholder="Username" :icon="User" type="text" />
        <InputField v-model="email" name="email" placeholder="Email" :icon="Mail" type="email" />
        <InputField v-model="name" name="name" placeholder="Name" :icon="IdCard" type="text" />

        <InputField v-model="password" name="password" placeholder="Password" :icon="KeySquare" type="password" />
        <p v-if="error" class="text-sm text-red-500">{{ error }}</p>
        <p v-if="success" class="text-sm text-green-500">{{ success }}</p>
        <RouterLink to="/" class="text-sm text-[#1F2937]/75">Already
          have an account? <span class="underline">Login</span></RouterLink>
        <PrimaryButton type="submit" class="mt-8 w-full">Register</PrimaryButton>
      </form>

      <!-- <button
        class="ml-auto text-white bg-[#17313E] py-1.5 lg:px-4 md:px-4 px-2 text-sm rounded-md cursor-pointer hover:bg-[#17313E]/90 duration-150 ease-in-out font-medium flex items-center justify-center">Login</button> -->
    </div>
  </section>
</template>
