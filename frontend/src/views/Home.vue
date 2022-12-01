<script setup lang="ts">
import QuizCard from '@/components/QuizCard.vue';
import { useRouter } from 'vue-router';

const router = useRouter();
function goToQuiz(quizId: number) {
    router.push({ path: `/quiz/${quizId}` });
}
</script>

<template>
    <div class="home-container">
        <div class="">
            <h1>Get Started</h1>
        </div>
        <!-- Quiz details will be inserted as attributes to QuizCard components
            for each quiz in quizzes list -->
        <div v-for="num in 7" :key="num">
            <QuizCard @click="goToQuiz(num)" />
        </div>
    </div>
</template>

<style scoped>
.home-container {
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: center;
    width: 100%;
    padding-bottom: 30px;
}
</style>
