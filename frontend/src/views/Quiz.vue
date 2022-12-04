<script setup lang="ts">
import { withDefaults, ref, computed } from 'vue';
import type { Ref, ComputedRef } from 'vue';
import type {Quizoot} from '@schemas/interface';
import QuizPreview from '@/components/QuizPreview.vue';
import QuestionWrapper from '@/components/QuestionWrapper.vue';
import quiz from '@/data/quiz-data-types.json';

interface QuizProps {
    data: Quizoot.Quiz;
}

const props = withDefaults(defineProps<QuizProps>(), {
    data: () => quiz as Quizoot.Quiz,
});

const currentQuestionIndex: Ref<number | null> = ref(null);

const questionsFlow: ComputedRef = computed(() => {
    return {
        isFirstQuestion: currentQuestionIndex.value == 0,
        isLastQuestion: currentQuestionIndex.value == props.data.questions.length - 1
    }
});

function startQuiz() {
    currentQuestionIndex.value = 0;
}

function goToNextQuestion() {
    if (currentQuestionIndex.value != null && currentQuestionIndex.value < props.data.questions.length - 1) {
        currentQuestionIndex.value++;
    }
}

function goToPreviousQuestion() {
    if (currentQuestionIndex.value != null && currentQuestionIndex.value > 0) {
        currentQuestionIndex.value--;
    }
}
</script>

<template>
    <div class="quiz-container">
        <h1 class="quiz-title">{{ props.data.title }}</h1>
        <br />
        <QuizPreview
            v-if="currentQuestionIndex == null"
            :questionsCount="props.data.questions.length"
            :description="props.data.description"
            :authors="props.data.authors"
            :onStart="startQuiz"
        />
        <question-wrapper
                v-else
                :question="props.data.questions[currentQuestionIndex]"
                :questionsCount="props.data.questions.length"
                :questionsFlow="questionsFlow"
                :goToNextQuestion="goToNextQuestion"
                :goToPreviousQuestion="goToPreviousQuestion"
        >
        </question-wrapper>
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
        margin-inline: 5%;
    }
}

.quiz-title {
    margin-bottom: 0;
}
</style>
