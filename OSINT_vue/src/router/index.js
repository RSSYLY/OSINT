import { createRouter, createWebHistory } from 'vue-router'
import IndexView from "@/views/IndexView.vue";
import LoginView from '@/views/login/LoginView.vue'
import SignupView from "@/views/login/SignupView.vue";
import FindPassView from "@/views/login/FindPassView.vue";
import DashboardMainView from "@/views/main/DashboardMainView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'index',
      component: IndexView
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignupView
    },
    {
      path:'/findpass',
      name:'findpass',
      component:FindPassView
    },
    {
      path:'/dashboard',
      name:'dashboardMain',
      component: DashboardMainView,
      children:[
        {
          path:'/global',
          name:'global',
          component:()=>import('@/views/dashboard/DashboardView.vue')
        },
        {
          path:'profile',
          name:'profile',
          component:()=>import('@/views/dashboard/ProfileView.vue')
        },
        {
          path:'settings',
          name:'settings',
          component:()=>import('@/views/dashboard/SettingsView.vue')
        },
        {
          path:'about',
          name:'about',
          component:()=>import('@/views/dashboard/AboutView.vue')
        }
      ],
    }
  ]
})

export default router
