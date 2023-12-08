
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import {useMainStore} from "@/store/store.js";
import App from './App.vue'
import router from './router'
import 'mdui/mdui.css';
import 'mdui';
import axios from "axios";

const app = createApp(App)
// 使用pinia作为store
const pinia = createPinia()
// 设置axios的默认基础URL
axios.defaults.baseURL = 'http://127.0.0.1:8000';
// 将axios挂载到Vue实例的原型链上
app.config.globalProperties.$axios = axios;
app.use(pinia)
app.use(router)
app.mount('#app')
