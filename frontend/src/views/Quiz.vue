<script setup lang="ts">
import { withDefaults, ref, computed } from 'vue';
import type { Ref, ComputedRef } from 'vue';
import type { Quizoot } from '@schemas/interface';
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
        questionNumber:
            currentQuestionIndex.value == null
                ? 0
                : currentQuestionIndex.value + 1,
        isFirstQuestion: currentQuestionIndex.value == 0,
        isLastQuestion:
            currentQuestionIndex.value == props.data.questions.length - 1,
    };
});

function startQuiz() {
    currentQuestionIndex.value = 0;
}

function quitQuiz() {
    currentQuestionIndex.value = null;
}

function goToNextQuestion() {
    if (
        currentQuestionIndex.value != null &&
        currentQuestionIndex.value < props.data.questions.length - 1
    ) {
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
        <h1 class="quiz-title">
            <span class="back-to-quiz-preview-icon">
                <font-awesome-icon
                    v-show="currentQuestionIndex != null"
                    @click="quitQuiz"
                    icon="fa-solid fa-chevron-left"
                /> </span
            >{{ props.data.title }}
        </h1>
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

<style scoped>
.quiz-container {
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: center;
}

.quiz-container .quiz-title {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    height: fit-content;
    margin-top: 1em;
}

.quiz-container .quiz-title .back-to-quiz-preview-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 0.8em;
    aspect-ratio: 1 / 1;
    color: var(--main-purple-lightened);
}

.quiz-container .quiz-title .back-to-quiz-preview-icon:hover {
    color: var(--palette-carribean-green);
}

.quiz-container .quiz-title .back-to-quiz-preview-icon > * {
    width: 100%;
    height: 100%;
}

.quiz-container .quiz-title {
    cursor: pointer;
    text-align: left;
    flex: 1;
}

.quiz-container .quiz-title h1 {
    margin: 0;
}

.quiz-container h1.quiz-title {
    margin-bottom: 0;
}

@media only screen and (max-width: 600px) {
    .quiz-container {
        margin-inline: 5%;
    }

    .quiz-container .quiz-title .back-to-quiz-preview-icon {
        width: 1.25em;
    }
}
</style>
