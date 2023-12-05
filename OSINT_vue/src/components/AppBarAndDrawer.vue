<script>
import {computed, inject} from 'vue'
import { useMainStore } from '@/store/store.js'
import {getTheme, setTheme} from "mdui";

export default {
  setup() {
    //获取响应式Store
    const store = useMainStore();
    return {
      store: store
    }

  },
  methods: {
    // 切换抽屉
    toggleDrawer() {
      const drawer = document.querySelector('.main-navigation-drawer')
      drawer.open = !drawer.open
    },
    // 切换日夜主题
    changeTheme(themeValue) {
      localStorage.setItem("theme", themeValue);
      setTheme(localStorage.getItem("theme"));
    }
  },
  data() {
    return {
      theme: getTheme()
    }
  }
}
</script>

<template>
  <mdui-navigation-drawer class="main-navigation-drawer">
    <mdui-list>
      <mdui-list-item>Navigation drawer</mdui-list-item>
    </mdui-list>
  </mdui-navigation-drawer>
  <mdui-top-app-bar class="top-app-bar" scroll-behavior="elevate" scroll-target=".layout-main">
    <mdui-button-icon icon="menu" @click="toggleDrawer"></mdui-button-icon>
    <mdui-top-app-bar-title>{{store.pageInfo.title}}</mdui-top-app-bar-title>
    <div style="flex-grow: 1"></div>
    <mdui-dropdown trigger="click" placement="auto" open-delay="150" close-delay="150">
      <mdui-button-icon icon="color_lens" slot="trigger"></mdui-button-icon>
      <mdui-menu selects="single" :value="theme">
        <mdui-menu-item @click="changeTheme('auto')" value="auto">自动</mdui-menu-item>
        <mdui-menu-item @click="changeTheme('light')" value="light">日间</mdui-menu-item>
        <mdui-menu-item @click="changeTheme('dark')" value="dark">夜间</mdui-menu-item>
      </mdui-menu>
    </mdui-dropdown>
  </mdui-top-app-bar>
</template>

<style scoped>

</style>