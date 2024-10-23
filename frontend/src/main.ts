import './assets/main.css'
import 'https://yastatic.net/s3/passport-sdk/autofill/v1/sdk-suggest-with-polyfills-latest.js';     

import { createApp } from 'vue'
import App from './App.vue'
import router from './routes/index'
// import Vue from 'vue'
// import Vuex from 'vuex'

createApp(App)
    .use(router)
    .mount('#app');
