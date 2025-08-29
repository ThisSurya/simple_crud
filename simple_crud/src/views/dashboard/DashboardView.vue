<script setup lang="ts">
import DeleteButton from '@/components/buttons/DeleteButton.vue'
import PrimaryButton from '@/components/buttons/PrimaryButton.vue'
import InputField from '@/components/InputField.vue'
import type { InterfaceUser } from '@/interface/InterfaceUser'
import { RequestHttp } from '@/util/Request'
import { PencilLine, Trash2 } from 'lucide-vue-next'
import { onMounted, ref, watch } from 'vue'
import { useRouter } from 'vue-router'

const users = ref<InterfaceUser[]>([])
const sort_by = ref('id')
const order = ref<'asc' | 'desc'>('asc')
const search = ref('')
const loading = ref(false)
const router = useRouter()

onMounted(GetData)

async function GetData() {
  loading.value = true
  try {
    const response = await RequestHttp({
      type: 'get',
      url: ``,
      params: { sort_by: sort_by.value, order: order.value, search: search.value }
    })
    if (response.status === 'failed') return
    users.value = response.data
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

async function DeleteUser(id: number) {
  try {
    await RequestHttp({ type: 'delete', url: `/users/${id}` })
    GetData()
  } catch (e) {
    console.error(e)
  }
}

async function Logout() {
  try {
    // Opsional: panggil API logout bila ada
    // await RequestHttp({ type: 'post', url: '/logout' })
  } catch (e) {
    console.error(e)
  } finally {
    localStorage.removeItem('token') // sesuaikan key
    localStorage.removeItem('username') // sesuaikan key
    router.push('/') // sesuaikan path login
  }
}

watch([sort_by, order, search], GetData)
</script>

<template>
  <div class="flex flex-col items-center gap-y-8 w-full max-w-[2560px]">
    <h1 class="text-3xl font-semibold text-[#17313E]">
      Welcome to the Dashboard
    </h1>

    <div
      class="w-full max-w-7xl bg-white/80 backdrop-blur rounded-2xl shadow-sm ring-1 ring-[#415E72]/10 px-8 py-6 space-y-6">

      <div class="flex flex-wrap items-center gap-5 bg-[#C5B0CD]/20 border border-[#C5B0CD]/40 rounded-lg px-4 py-3">
        <!-- Order -->
        <label class="text-xs font-medium uppercase tracking-wide text-[#415E72]">
          Order
          <select v-model="order"
            class="ml-2 text-sm rounded-md border border-[#415E72]/30 bg-white/60 focus:outline-none focus:ring-2 focus:ring-[#C5B0CD] px-2 py-1">
            <option value="asc">Asc</option>
            <option value="desc">Desc</option>
          </select>
        </label>

        <div class="flex flex-col gap-1">
          <p class="text-xs font-medium uppercase tracking-wide text-[#415E72]">Sort By</p>
          <div class="flex gap-2">
            <label v-for="value in ['name', 'username', 'email']" :key="value"
              class="cursor-pointer flex items-center gap-1.5">
              <input type="radio" class="" name="sort_by" :value="value" v-model="sort_by" />
              <!-- <span class="inline-flex items-center rounded-full px-3 py-1 text-xs font-medium
                       border border-[#415E72]/30 text-[#415E72] bg-white/60
                       peer-checked:bg-[#415E72] peer-checked:text-white peer-checked:border-[#415E72]
                       transition">
                {{ value }}
              </span> -->
              <span class="text-xs font-medium text-[#415E72] accent-[#415E72]">{{ value }}</span>
            </label>
          </div>
        </div>

        <!-- Search -->
        <div class="ml-auto flex items-center gap-3">
          <div class="w-64">
            <InputField v-model="search" placeholder="Search..." type="text" class="text-sm" />
          </div>
          <DeleteButton @click="Logout" class="px-4 py-1.5 text-sm bg-[#17313E] hover:bg-[#17313E]/90">
            Logout
          </DeleteButton>
        </div>
      </div>

      <!-- Data Grid -->
      <div class="rounded-xl overflow-hidden ring-1 ring-[#415E72]/15">
        <!-- Header -->
        <div class="grid grid-cols-5 bg-gradient-to-r from-[#17313E] to-[#415E72] text-white text-sm font-medium">
          <div class="p-3">No</div>
          <div class="p-3">Name</div>
          <div class="p-3">Username</div>
          <div class="p-3">Email</div>
          <div class="p-3">Act</div>
        </div>

        <!-- States -->
        <div v-if="loading" class="p-6 text-center text-sm text-[#415E72] bg-white">
          Loading...
        </div>
        <div v-else-if="!users.length" class="p-6 text-center text-sm text-[#415E72] bg-white">
          No users found.
        </div>

        <!-- Rows -->
        <div v-else>
          <div v-for="(user, i) in users" :key="user.id"
            class="grid grid-cols-5 bg-white/70 even:bg-[#C5B0CD]/10 hover:bg-[#C5B0CD]/25 transition-colors text-sm">
            <div class="p-3 font-medium text-[#17313E]">{{ i + 1 }}</div>
            <div class="p-3 text-[#17313E]">{{ user.name }}</div>
            <div class="p-3 text-[#415E72]">{{ user.username }}</div>
            <div class="p-3 text-[#415E72]">{{ user.email }}</div>
            <div class="p-3 flex items-center gap-2">
              <RouterLink :to="`/edit/${user.id}`">
                <PrimaryButton class="px-2.5 py-1.5 text-xs">
                  <PencilLine class="stroke-white size-4" />
                </PrimaryButton>
              </RouterLink>
              <DeleteButton @click="DeleteUser(user.id)"
                class="px-2.5 py-1.5 text-xs bg-[#C5B0CD] hover:bg-[#C5B0CD]/90">
                <Trash2 class="stroke-white size-4" />
              </DeleteButton>
            </div>
          </div>
        </div>
      </div>

      <!-- Footer (optional) -->
      <div class="text-[11px] text-[#415E72]/70 tracking-wide text-right">
        Total: {{ users.length }} user(s)
      </div>
    </div>
  </div>
</template>
