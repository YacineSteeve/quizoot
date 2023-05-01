import { createRouter, createWebHistory } from 'vue-router';
import type { RouteRecordRaw } from 'vue-router';

const routes: Array<RouteRecordRaw> = [
    {
        path: '/',
        name: 'Home',
        component: () => import('@/views/Home.vue'),
    },
    {
        path: '/quiz/:id',
        name: 'Quiz',
        component: () => import('@/views/Quiz.vue'),
    },
    {
        path: '/admin',
        name: 'Admin',
        component: () => import('@/views/admin/Admin.vue'),
        children: [
            {
                path: '',
                name: 'Landing',
                component: () => import('@/views/admin/Landing.vue'),
            },
            {
                path: 'quizzes',
                name: 'Quizzes',
                component: () => import('@/views/admin/Quizzes.vue'),
            },
            {
                path: 'questions',
                name: 'Questions',
                component: () => import('@/views/admin/Questions.vue'),
            },
        ],
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;
