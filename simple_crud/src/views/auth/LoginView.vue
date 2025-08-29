<script setup lang="ts">
// import
import PrimaryButton from '@/components/buttons/PrimaryButton.vue';
import InputField from '@/components/InputField.vue';
import { RequestHttp } from '@/util/Request';
import axios from 'axios';
import { KeySquare, User } from 'lucide-vue-next';
import { ref } from 'vue';
import { useRouter } from 'vue-router'
const router = useRouter();
const username = ref('');
const password = ref('');
const error = ref('');
const success = ref('');

// validation username & password
function validate() {
  if (username.value === '' || password.value === '') {
    error.value = 'Username and password are required';
    return false;
  }
  return true;
}

async function OnSubmit(e: Event) {
  e.preventDefault();
  error.value = '';
  // handle submit
  if (!validate()) return;
  console.log(import.meta.env.VITE_API_URL)
  const resp = await RequestHttp({
    type: 'post',
    url: `/login`,
    datas: {
      username: username.value,
      password: password.value,
    }
  });

  if (resp.status === 'failed') {
    error.value = 'Invalid username or password';
    return;
  }

  success.value = 'Login successful! Redirecting to dashboard...';
  // get token from response
  const token = resp.data.access_token;
  localStorage.setItem('token', token);
  localStorage.setItem('username', resp.data.username);
  // localStorage.setItem('exp', new)
  router.push('/dashboard');
}

</script>

<template>
  <section class="bg-white rounded-xl gap-x-4 flex items-center justify-center m-auto overflow-hidden min-h-[325px]">
    <div class="flex flex-col p-4 px-6 gap-y-7 w-[350px]">
      <div class="space-y-2">
        <h1 class="text-2xl font-semibold text-[#1F2937] text-center">Simple Dashboard</h1>
        <p class="text-xs text-[#1F2937]/75 text-center">Login page</p>
      </div>
      <form @submit.prevent="OnSubmit" class="space-y-3">
        <InputField v-model="username" name="username" placeholder="Username" :icon="User" type="text" />

        <InputField v-model="password" name="password" placeholder="Password" :icon="KeySquare" type="password" />
        <p v-if="error" class="text-sm text-red-500">{{ error }}</p>
        <p v-if="success" class="text-sm text-green-500">{{ success }}</p>
        <RouterLink to="/register" class="text-sm text-[#1F2937]/75">Don't
          have an account? <span class="underline">Register</span></RouterLink>
        <PrimaryButton :type="'submit'" class="mt-8 w-full">Login</PrimaryButton>
      </form>

      <!-- <button
        class="ml-auto text-white bg-[#17313E] py-1.5 lg:px-4 md:px-4 px-2 text-sm rounded-md cursor-pointer hover:bg-[#17313E]/90 duration-150 ease-in-out font-medium flex items-center justify-center">Login</button> -->
    </div>
  </section>
</template>
