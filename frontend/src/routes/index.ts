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
import InfoView from "@/views/InfoView.vue";
import SearchView from "@/views/SearchView.vue";
import AddFlourView from "@/views/AddFlourView.vue";


const routesAuth = [
    {path: '/auth/', component: AuthView},
    {path: '/', component: DisplayView},
    {path: '/search/', component: SearchView},
    {path: '/info/', component: InfoView},
    {path: '/auth/login/', component: AuthLoginView},
    {path: '/auth/register/', component: AuthRegisterView},
    {path: '/auth/recover/', component: AuthRecoverView},
]

const routesBooking = [
    {path: '/book/', component: BookView},
    {path: '/test-page/', component: TestPageView},
    {path: '/book-history/', component: BookHistoryView}
]

const routesProfile = [
    {path: '/profile/', component: ProfileView}
]

const routesAudiences = [
    {path: '/add_new_flour/', component: AddFlourView}
]

const routes = [
    ...routesAuth, ...routesBooking, ...routesProfile, ...routesAudiences
]

const router = createRouter({
    history: createWebHistory(),
    routes: routes,
})

// export default router;

export default router;


// export default {
//   data() {
//     return {
//       sharedVariable: 'значение переменной'
//     }
//   }
// };
