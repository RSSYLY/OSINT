<script>
import {computed, inject} from 'vue'
import { useMainStore } from '@/store/store.js'

export default {
  setup() {
    //获取响应式Store
    const store = useMainStore();
    return {
      $store: store
    }

  },
  methods: {
    // 切换抽屉
    toggleDrawer() {
      const drawer = document.querySelector('.main-navigation-drawer')
      drawer.open = !drawer.open
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
    <mdui-top-app-bar-title>{{$store.pageInfo.title}}</mdui-top-app-bar-title>
    <div style="flex-grow: 1"></div>
    <mdui-button-icon icon="more_vert"></mdui-button-icon>
  </mdui-top-app-bar>
</template>

<style scoped>

</style>