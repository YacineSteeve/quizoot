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
                path: 'quizzes/edit/:id?',
                name: 'QuizCreate',
                component: () => import('@/views/admin/quizzes/QuizEdit.vue'),
                props: (route) => ({
                    data: JSON.parse(route.query.data),
                }),
            },
            {
                path: 'questions',
                name: 'Questions',
                component: () =>
                    import('@/views/admin/questions/Questions.vue'),
            },
            {
                path: 'questions/edit/:id?',
                name: 'QuestionEdit',
                component: () =>
                    import('@/views/admin/questions/QuestionEdit.vue'),
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
