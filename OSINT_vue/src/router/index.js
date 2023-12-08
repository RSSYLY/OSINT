import { createRouter, createWebHistory } from 'vue-router'
import IndexView from "@/views/IndexView.vue";
import LoginView from '@/views/login/LoginView.vue'
import SignupView from "@/views/login/SignupView.vue";
import FindPassView from "@/views/login/FindPassView.vue";
import DashboardMainView from "@/views/main/DashboardMainView.vue";
import {useMainStore} from "@/store/store";
import axios from "axios";
import {snackbar} from "mdui";

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
      path:'/logout',
      name:'logout',
      component:()=>import('@/views/login/LogoutView.vue')
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

// 路由守卫实现登录验证
router.beforeEach((to, from, next) => {

  // 从store中获取用户信息
  const userInfo = useMainStore().userInfo;
  const userStatus = useMainStore().userStatus;


  if (userStatus.isLogin && userInfo.token) {
    const postToken = {token: userInfo.token,id:userInfo.id};
    // 当token存在且为登录状态（userStatue==true）时，向后端发送token和用户id，验证token是否有效
    // （id和token对应验证功能暂未实现，似乎没有实现的必要）
    // router请求时，全局axios后挂载到Vue实例的原型链上，所以这里不能用this.$axios，而是直接使用axios，同时也得再写一遍后端地址
    axios.post('http://127.0.0.1:8000/authenticate/is-token-valid/', postToken)
        .then((response) => {
          console.debug('token验证返回数据：',response.data)
          if (response.data.error === 0) {
            // token有效，放行
            console.debug('token有效，放行')
            // 但如果登录后再访问登录、注册、找回密码页面，需要重定向到控制台
            if (to.path === '/login' || to.path === '/signup' || to.path === '/findpass') {
              console.debug('登录后再访问登录、注册、找回密码页面，重定向到控制台')
              next('/dashboard');
            } else {
              next();
            }
          } else {
            // token无效，重定向到登录页,清除store中的用户信息
            userStatus.isLogin = false;
            userInfo.id = 0;
            userInfo.username = "";
            userInfo.email = "";
            userInfo.phone = "";
            userInfo.token = "";
            userInfo.is_superuser = false;
            userInfo.is_staff = false;
            userInfo.is_active = false;
            // 清除localStorage中的用户信息
            localStorage.removeItem('token');
            //
            console.debug('token无效，重定向到登录页');
            next('/login');

          }
        })
        .catch((error) => {
          // 后端错误
            console.error('token验证后端请求失败',error);
          snackbar({
            message: "内部错误",
          });
        });
  } else {
    // 没token或非登录状态
    // 将store中的用户信息清除
    userStatus.isLogin = false;
    userInfo.id = 0;
    userInfo.username = "";
    userInfo.email = "";
    userInfo.phone = "";
    userInfo.token = "";
    userInfo.is_superuser = false;
    userInfo.is_staff = false;
    userInfo.is_active = false;
    // 清除localStorage中的用户信息
    localStorage.removeItem('token');
    // 对于没有token或非登录状态的情况，直接放行的页面有：登录、注册、找回密码，其他页面重定向到登录页
    console.debug('没有token或非登录状态')
    if (to.path === '/login' || to.path === '/signup' || to.path === '/findpass') {
      // 登录、注册、找回密码页面不需要登录，直接放行
      next();
    } else {
      // 其他页面需要登录，重定向到登录页
      next('/login');
    }
  }
});

