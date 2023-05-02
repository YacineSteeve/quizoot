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
                component: () => import('@/views/admin/quizzes/Quizzes.vue'),
            },
            {
                path: 'quizzes/create',
                name: 'QuizCreate',
                component: () => import('@/views/admin/quizzes/QuizEdit.vue'),
            },
            {
                path: 'quizzes/:id',
                name: 'QuizEdit',
                component: () => import('@/views/admin/quizzes/QuizEdit.vue'),
            },
            {
                path: 'questions',
                name: 'Questions',
                component: () => import('@/views/admin/questions/Questions.vue'),
            },
            {
                path: 'questions/create',
                name: 'QuestionCreate',
                component: () => import('@/views/admin/questions/QuestionEdit.vue'),
            },
            {
                path: 'questions/:id',
                name: 'QuestionEdit',
                component: () => import('@/views/admin/questions/QuestionEdit.vue'),
            },
        ],
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;
