import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/login/LoginView.vue'
import SignonView from "@/views/login/SignonView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'home',
      component: LoginView
    },
    {
      path: '/signon',
      name: 'signon',
      component: SignonView
    }
  ]
})

export default router
