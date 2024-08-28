import {createRouter, createWebHistory} from 'vue-router'
import BookView from "@/views/BookView.vue";
import AuthView from "@/views/AuthView.vue";
import AuthLoginView from "@/views/AuthLoginView.vue";
import AuthRegisterView from "@/views/AuthRegisterView.vue";
import AuthRecoverView from "@/views/AuthRecoverView.vue";

const routesAuth = [
    {path: '/auth/', component: AuthView},
    {path: '/auth/login/', component: AuthLoginView},
    {path: '/auth/register/', component: AuthRegisterView},
    {path: '/auth/recover/', component: AuthRecoverView},
]

const routesBooking = [
    {path: '/', component: BookView},
]

const routes = [
    ...routesAuth, ...routesBooking
]


const router = createRouter({
    history: createWebHistory(),
    routes: routes,
})

export default router;