
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import {useMainStore} from "@/store/store.js";
import App from './App.vue'
import router from './router'
import 'mdui/mdui.css';
import 'mdui';

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)
app.mount('#app')
