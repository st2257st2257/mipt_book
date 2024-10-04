import {createRouter, createWebHistory} from 'vue-router'
import TestPageView from "@/views/TestPageView.vue";
import BookView from "@/views/BookView.vue";
import AuthView from "@/views/AuthView.vue";
import AuthLoginView from "@/views/AuthLoginView.vue";
import AuthRegisterView from "@/views/AuthRegisterView.vue";
import AuthRecoverView from "@/views/AuthRecoverView.vue";
import BookHistoryView from "@/views/BookHistoryView.vue";
import ProfileView from "@/views/ProfileView.vue";
import DisplayView from "@/views/DisplayView.vue";

const routesAuth = [
    {path: '/auth/', component: AuthView},
    {path: '/display/', component: DisplayView},
    {path: '/auth/login/', component: AuthLoginView},
    {path: '/auth/register/', component: AuthRegisterView},
    {path: '/auth/recover/', component: AuthRecoverView},
]

const routesBooking = [
    {path: '/', component: BookView},
    {path: '/test-page/', component: TestPageView},
    {path: '/book-history/', component: BookHistoryView}
]

const routesProfile = [
    {path: '/profile/', component: ProfileView}
]

const routes = [
    ...routesAuth, ...routesBooking, ...routesProfile
]


const router = createRouter({
    history: createWebHistory(),
    routes: routes,
})

export default router;
