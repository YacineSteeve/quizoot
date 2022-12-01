<script setup lang="ts">
import { defineProps, withDefaults, ref } from 'vue';
import type { Ref } from 'vue';
import QuizPreview from '@/components/QuizPreview.vue';
import QuestionWrapper from '@/components/questions/QuestionWrapper.vue';
import type { Quizoot } from '@schemas/interface';
import quiz from '@/data/quiz-data-types.json';

interface QuizProps {
    data: Quizoot.Quiz;
}

withDefaults(defineProps<QuizProps>(), {
    data: () => quiz as Quizoot.Quiz,
});

const currentQuestion: Ref<number | null> = ref(null);
function startQuiz() {
    currentQuestion.value = 0;
}
</script>

<template>
    <div class="quiz-container">
        <h1 class="quiz-title">{{ data.title }}</h1>
        <QuizPreview
            v-if="currentQuestion == null"
            :questionsCount="data.questions.length"
            :description="data.description"
            :authors="data.authors"
            :onStart="startQuiz"
        />
        <QuestionWrapper v-else :question="data.questions[currentQuestion]" />
    </div>
</template>

<style>
.quiz-container {
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: center;
    width: 65%;
    margin-left: 17.5%;
    margin-right: 17.5%;
    padding-bottom: 30px;
    min-height: 60vh;
}

.quiz-title {
    margin-bottom: 0;
}
</style>
