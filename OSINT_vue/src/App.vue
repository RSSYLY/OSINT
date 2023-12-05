<script>
import { RouterLink, RouterView } from 'vue-router'
import TopAppBar from "@/components/AppBarAndDrawer.vue";
export default {
  components: {
    TopAppBar,RouterView
  }
}

</script>

<template>
  <mdui-layout>
    <TopAppBar/>
    <mdui-layout-main style="min-height: 300px">
      <main class="layout-main"><RouterView/></main>
    </mdui-layout-main>
  </mdui-layout>
</template>

<style scoped>
mdui-layout{
  height: 100vh;
}
</style>