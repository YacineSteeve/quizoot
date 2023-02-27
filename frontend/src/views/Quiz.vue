<script setup lang="ts">
import { ref, computed } from 'vue';
import { useRoute } from 'vue-router';
import type { Quizoot } from '@interfaces/quizoot';
import { useFetch } from '@/lib/hooks';
import { log } from '@/lib';
import QuizPreview from '@/components/QuizPreview.vue';
import Question from '@/components/Question.vue';
import QuestionsNavigation from '@/components/QuestionsNavigation.vue';
import FetchError from '@/components/FetchError.vue';
import Loader from '@/components/Loader.vue';

const route = useRoute();

const {
    data: quiz,
    isFetching,
    error,
} = useFetch<Quizoot.Quiz>(`/api/quizzes/${route.params.id}`);

const questions = computed(() => {
    return quiz.value?.questions ?? [];
});

const currentQuestion = ref(-1);

function getCurrentQuestion() {
    return questions.value[currentQuestion.value];
}

function startQuiz() {
    currentQuestion.value = 0;
}

function quitQuiz() {
    currentQuestion.value = -1;
}

function goToNextQuestion() {
    currentQuestion.value = Math.min(
        currentQuestion.value + 1,
        questions.value.length
    );
}

function goToPreviousQuestion() {
    currentQuestion.value = Math.max(0, currentQuestion.value - 1);
}

function submitQuiz() {
    // TODO
    alert('Quiz submitted!');
}
</script>

<template>
    <FetchError v-if="error" />
    <Loader v-else-if="isFetching" />
    <div v-else class="quiz-container">
        <h1 class="quiz-title">
            <span
                v-if="currentQuestion !== -1"
                class="back-to-quiz-preview-icon"
            >
                <font-awesome-icon
                    @click="quitQuiz"
                    icon="fa-solid fa-chevron-left"
                />
            </span>
            {{ quiz?.title }}
        </h1>
        <br />
        <QuizPreview
            v-if="currentQuestion === -1"
            :questionsCount="questions.length"
            :description="quiz?.description"
            :authors="quiz?.authors"
            :onStart="startQuiz"
        />
        <question
            v-if="currentQuestion !== -1"
            :id="getCurrentQuestion()"
            :totalQuestions="questions.length"
            :rank="currentQuestion + 1"
            :key="currentQuestion"
        >
        </question>
        <QuestionsNavigation
            v-if="currentQuestion !== -1"
            :showPrevious="currentQuestion > 0"
            :showNext="currentQuestion + 1 < questions.length"
            :goToNextQuestion="goToNextQuestion"
            :goToPreviousQuestion="goToPreviousQuestion"
            :submit="submitQuiz"
        />
    </div>
</template>

<style scoped>
.quiz-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 80%;
    margin: 0;
}

.quiz-container .quiz-title {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    gap: 20px;
    margin-top: 0.5em;
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
    color: var(--main-purple);
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

    .quiz-container .quiz-title {
        position: relative;
        text-align: center;
    }

    .quiz-container .quiz-title .back-to-quiz-preview-icon {
        position: absolute;
        left: -1em;
        width: 1em;
    }
}
</style>
