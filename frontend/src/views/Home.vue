<script setup lang="ts">
import QuizCard from '@/components/QuizCard.vue';
import { useRouter } from 'vue-router';
import { useFetch } from '@/lib/hooks';
import type { Quizoot } from '@interfaces/quizoot';

const router = useRouter();

const { data: quizzes } = useFetch<Quizoot.Quiz[]>('/api/quizzes');

function goToQuiz(quizId: Quizoot.Quiz['id']) {
    router.push({ path: `/quiz/${quizId}` });
}
</script>

<template>
    <div class="home-container">
        <div class="">
            <h1>Get Started</h1>
        </div>
        <div v-for="quiz in quizzes" :key="quiz.id">
            <QuizCard
                :title="quiz.title"
                :description="quiz.description"
                @click="goToQuiz(quiz.id)"
            />
        </div>
    </div>
</template>

<style scoped>
.home-container {
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    width: 100%;
    min-height: 100vh;
    padding-bottom: 30px;
}
</style>
