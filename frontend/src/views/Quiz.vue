<script setup lang="ts">
import { defineProps, withDefaults, ref } from 'vue';
import type { Ref } from 'vue';
import QuizPreview from '@/components/QuizPreview.vue';
import Question from '@/components/Question.vue';
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
        <br/>
        <QuizPreview
            v-if="currentQuestion == null"
            :questionsCount="data.questions.length"
            :description="data.description"
            :authors="data.authors"
            :onStart="startQuiz"
        />
        <Question v-else :question="data.questions[currentQuestion]" />
    </div>
</template>

<style>
.quiz-container {
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: center;
}

@media only screen and (max-width: 600px) {
    .quiz-container {
        margin-inline: 5%
    }
}

.quiz-title {
    margin-bottom: 0;
}
</style>
