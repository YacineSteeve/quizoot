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
                path: ':elements',
                name: 'List',
                component: () => import('@/views/admin/List.vue'),
            },
            {
                path: 'quizzes/edit/:id?',
                name: 'QuizCreate',
                component: () => import('@/views/admin/edit/QuizEdit.vue'),
                props: (route) => ({
                    data: JSON.parse(route.query.data),
                }),
            },
            {
                path: 'questions/edit/:id?',
                name: 'QuestionEdit',
                component: () => import('@/views/admin/edit/QuestionEdit.vue'),
                props: (route) => ({
                    data: JSON.parse(route.query.data),
                }),
            },
        ],
    },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;
