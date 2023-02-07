<script setup lang="ts">
import QuizCard from '@/components/QuizCard.vue';
import { computed } from 'vue';
import type { ComputedRef } from 'vue';
import { useRouter } from 'vue-router';
import { useStore } from '@/store/store';
import { useFetch } from '@/lib/hooks';
import { log } from '@/lib';
import type { Quiz } from '@interfaces/quizoot.indexed';
import { MutationTypes } from '@/store/types';

const router = useRouter();
const store = useStore();

if (!store.state.quizzes) {
    useFetch<Quiz[]>('/api/quizzes')
        .then((response) => {
            if (response.error.value) {
                log(response.error.value);
            }

            store.commit(MutationTypes.UPDATE_QUIZZES, response.data.value);
        })
        .catch((error) => log(error));
}

const quizzes: ComputedRef<Quiz[] | null> = computed(() => store.state.quizzes);

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
        <div v-for="quiz in quizzes" :key="quiz">
            <QuizCard @click="goToQuiz(quiz.id)" />
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
