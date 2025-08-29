import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '@/views/auth/LoginView.vue'
import RegisterView from '@/views/auth/RegisterView.vue'
import DashboardView from '@/views/dashboard/DashboardView.vue'
import UpdateUserView from '@/views/dashboard/UpdateUserView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'login',
      component: LoginView,
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView,
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: DashboardView,
      meta: { requiresAuth: true },
    },
    {
      path: '/edit/:id',
      name: 'Update User',
      component: UpdateUserView,
      meta: { requiresAuth: true },
    },
  ],
})

// middleware global (navigation guard)
router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem('token') // contoh auth

  if (to.meta.requiresAuth && !isAuthenticated) {
    next({ name: 'login' }) // redirect ke login
  } else {
    next() // lanjut
  }
})

export default router
