<script setup lang="ts">
// import
import PrimaryButton from '@/components/buttons/PrimaryButton.vue';
import InputField from '@/components/InputField.vue';
import type { InterfaceUser } from '@/interface/InterfaceUser';
import { RequestHttp } from '@/util/Request';
import { ChevronLeft, IdCard, KeySquare, Mail, User } from 'lucide-vue-next';
import { onMounted, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';

const router = useRouter();
const route = useRoute();
const userId = ref<number | null>(null);

const username = ref('');
const password = ref('');
const name = ref('');
const email = ref('');
const error = ref('');
const success = ref('');
// const users = ref<InterfaceUser>();
const loading = ref(false)


function validate() {
  if (username.value === '' || name.value === '' || email.value === '') {
    error.value = 'Username, Name, and Email are required';
    return false;
  }

  if (password.value !== '' && password.value.length < 8) {
    error.value = 'Password must be at least 8 characters if provided';
    return false;
  }
  return true;
}

// async function OnSubmit(e: Event) {
//   e.preventDefault();
//   error.value = '';
//   if (!validate()) return;

//   if (password.value === '') {
//     // If password is empty, do not include it in the update
//     const result = await RequestHttp({
//       type: 'put',
//       url: `/users/${userId.value}`,
//       datas: {
//         username: username.value,
//         name: name.value,
//         email: email.value,
//       }
//     });
//   } else {
//     const result = await RequestHttp({
//       type: 'put',
//       url: `/users/${userId.value}`,
//       datas: {
//         username: username.value,
//         password: password.value,
//         name: name.value,
//         email: email.value,
//       }
//     });
//   }

//   if (result.status === 'failed') {
//     error.value = result.message || 'Registration failed';
//     return;
//   }

//   console.log('Registration successful:', result.data);
//   // Optionally, redirect to login page or clear form
//   username.value = '';
//   password.value = '';
//   name.value = '';
//   email.value = '';
//   router.push('/');
// }

async function OnSubmit(e: Event) {
  e.preventDefault();
  error.value = '';
  if (!validate()) return;

  const datas: any = {
    username: username.value,
    name: name.value,
    email: email.value
  };

  if (password.value) {
    datas.password = password.value;
  }

  const result = await RequestHttp({
    type: 'put',
    url: `/users/${userId.value}`,
    datas
  });

  if (result.status === 'failed') {
    error.value = result.message || 'Registration failed';
    return;
  }

  success.value = 'User updated successfully! Redirecting to dashboard...';
  // console.log('User updated successfully:', result.data);
  username.value = '';
  password.value = '';
  name.value = '';
  email.value = '';
  router.push('/dashboard');
}

onMounted(() => {
  if (route.params.id) {
    userId.value = Number(route.params.id);
    console.log('Editing user with ID:', route.params.id);
    GetData();
  }
});

async function GetData() {
  loading.value = true
  try {
    const response = await RequestHttp({
      type: 'get',
      url: `/users/${userId.value
        }`,
    })

    console.log(response.data);
    if (response.status == 'failed') return;

    // users.value = response.data;
    username.value = response.data.username;
    name.value = response.data.name;
    email.value = response.data.email;
  } catch (error) {
    console.error('Error fetching users:', error);
  } finally {
    loading.value = false
  }
}
</script>

<template>

  <section
    class="bg-white rounded-xl gap-x-4 flex flex-col items-center justify-center m-auto overflow-hidden min-h-[325px] ">


    <div class="flex flex-col gap-y-7 w-[350px] p-4 px-6">
      <div class="space-y-2">
        <h1 class="text-2xl font-semibold text-[#1F2937] text-center">Update User</h1>
        <p class="text-xs text-[#1F2937]/75 text-center">Fill all form that may update</p>
      </div>
      <RouterLink to="/dashboard" class="self-start">
        <PrimaryButton class="">
          Back
        </PrimaryButton>
      </RouterLink>

      <form @submit="OnSubmit" class="space-y-3">
        <InputField v-model="username" name="username" placeholder="Username" :icon="User" type="text" />
        <InputField v-model="email" name="email" placeholder="Email" :icon="Mail" type="email" />
        <InputField v-model="name" name="name" placeholder="Name" :icon="IdCard" type="text" />

        <InputField v-model="password" name="password" placeholder="Password" :icon="KeySquare" type="password" />
        <p v-if="error" class="text-sm text-red-500">{{ error }}</p>
        <p v-if="success" class="text-sm text-green-500">{{ success }}</p>
        <PrimaryButton type="submit" class="mt-8 w-full">Update data</PrimaryButton>
      </form>

      <!-- <button
        class="ml-auto text-white bg-[#17313E] py-1.5 lg:px-4 md:px-4 px-2 text-sm rounded-md cursor-pointer hover:bg-[#17313E]/90 duration-150 ease-in-out font-medium flex items-center justify-center">Login</button> -->

    </div>
  </section>
</template>
