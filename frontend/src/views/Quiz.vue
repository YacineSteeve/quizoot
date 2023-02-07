<script setup lang="ts">
import { ref, computed, onBeforeMount } from 'vue';
import type { Ref, ComputedRef } from 'vue';
import { useRoute } from 'vue-router';
import { useStore } from '@/store/store';
import { useFetch } from '@/lib/hooks';
import type { Quiz } from '@interfaces/quizoot.indexed';
import QuizPreview from '@/components/QuizPreview.vue';
import Question from '@/components/Question.vue';
import { log } from '@/lib';
import { MutationTypes } from '@/store/types';

const route = useRoute();
const store = useStore();

const errorOccurred: Ref<boolean> = ref(false);
const isFetchingQuiz: ComputedRef<boolean> = computed(
    () => store.state.currentQuiz === null
);

onBeforeMount(() => {
    useFetch<Quiz>(`/api/quizzes/${route.params.id}`)
        .then((response) => {
            if (response.error.value) {
                errorOccurred.value = true;
                console.log(response.error.value);
            } else {
                store.commit(
                    MutationTypes.UPDATE_CURRENT_QUIZ,
                    response.data.value
                );
            }
        })
        .catch((error) => {
            errorOccurred.value = true;
            log(error);
        });
});

const quiz = computed(() => store.state.currentQuiz);

const currentQuestionIndex: Ref<number | null> = ref(null);

const questionsFlow: ComputedRef = computed(() => {
    return {
        questionNumber:
            currentQuestionIndex.value == null
                ? 0
                : currentQuestionIndex.value + 1,
        isFirstQuestion: currentQuestionIndex.value == 0,
        isLastQuestion:
            currentQuestionIndex.value == quiz.value?.questions.length - 1,
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
        currentQuestionIndex.value < quiz.value?.questions.length - 1
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
    <div v-if="errorOccurred" class="quiz-fetch-error">
        <font-awesome-icon
            icon="fa-solid fa-triangle-exclamation"
            size="2xl"
            color="var(--main-purple-lightened)"
            class="warning-icon"
        />
        <br />
        <p>Sorry, something went wrong...</p>
    </div>
    <div v-else-if="isFetchingQuiz">
        <font-awesome-icon
            icon="fa-solid fa-spinner"
            size="2xl"
            color="var(--main-purple-lightened)"
            class="spinner"
        />
        <p>Loading...</p>
    </div>
    <div v-else class="quiz-container">
        <h1 class="quiz-title">
            <span
                v-if="currentQuestionIndex != null"
                class="back-to-quiz-preview-icon"
            >
                <font-awesome-icon
                    @click="quitQuiz"
                    icon="fa-solid fa-chevron-left"
                />
            </span>
            {{ quiz.title }}
        </h1>
        <br />
        <QuizPreview
            v-if="currentQuestionIndex == null"
            :questionsCount="quiz.questions.length"
            :description="quiz.description"
            :authors="quiz.authors"
            :onStart="startQuiz"
        />
        <question
            v-else
            :question="quiz.questions[currentQuestionIndex]"
            :questionsCount="quiz.questions.length"
            :questionsFlow="questionsFlow"
            :goToNextQuestion="goToNextQuestion"
            :goToPreviousQuestion="goToPreviousQuestion"
        >
        </question>
    </div>
</template>

<style scoped>
.quiz-fetch-error .warning-icon {
    font-size: 4em;
}

.quiz-fetch-error p {
    font-style: italic;
}

.quiz-container {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    width: 80%;
    margin: 0;
}

.spinner {
    animation: spin 1.65s linear infinite;
}

@keyframes spin {
    from {
        transform: rotate(0deg);
    }

    to {
        transform: rotate(360deg);
    }
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

    .quiz-container .quiz-title .back-to-quiz-preview-icon {
        width: 1.25em;
    }
}
</style>
