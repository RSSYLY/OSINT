<script>
import {setColorScheme,dialog,getTheme,setTheme,getColorFromImage} from "mdui";
import { RouterLink, RouterView } from 'vue-router'
import TopAppBar from "@/components/AppBarAndDrawer.vue";
import {useMainStore} from "@/store/store";
export default {
  components: {
    TopAppBar,RouterView
  },
  setup() {
    // 初始化localStorage
    if( localStorage.getItem("theme") === null){
      localStorage.setItem("theme","auto");
    }

    // 从localStorage中获取主题
    setTheme(localStorage.getItem("theme"));
    // 设置主题色
    setColorScheme("#2196f3");

    //从localStorage中获取token,若存在则将token存入store并设置登录状态为true
    const store = useMainStore();
    if(localStorage.getItem("token") !== null){
      store.userStatus.isLogin = true;
      store.userInfo.token = localStorage.getItem("token");
      console.debug("初始化：从浏览器存储获取Token成功")
    } else {
      store.userStatus.isLogin = false;
    }

  },
}

</script>

<template>
  <mdui-layout>
    <TopAppBar/>
    <mdui-layout-main style="min-height: 300px">
      <main class="layout-main">
        <RouterView/>
      </main>
    </mdui-layout-main>
  </mdui-layout>
</template>

<style scoped>
mdui-layout{
  height: 100vh;
}
</style>