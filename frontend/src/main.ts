import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './routes/index'
// import Vue from 'vue'
// import Vuex from 'vuex'

createApp(App)
    .use(router)
    .mount('#app');
