<script>
import {setColorScheme,dialog,getTheme,setTheme,getColorFromImage} from "mdui";
import { RouterLink, RouterView } from 'vue-router'
import TopAppBar from "@/components/AppBarAndDrawer.vue";
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