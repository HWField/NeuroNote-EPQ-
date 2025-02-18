import './assets/index.css'
import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import piniaPersist from "pinia-plugin-persistedstate";

import VSwatches from 'vue3-swatches'
import 'vue3-swatches/dist/style.css'
const pinia = createPinia()
pinia.use(piniaPersist);  // ✅ Enable persistence
const app = createApp(App)

app.use(VSwatches)
app.use(pinia)
app.use(router)

app.mount('#app')