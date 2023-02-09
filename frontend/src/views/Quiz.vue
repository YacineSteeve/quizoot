<script setup lang="ts">
import { ref, computed, onBeforeMount } from 'vue';
import type { Ref, ComputedRef } from 'vue';
import { useRoute } from 'vue-router';
import type { Quizoot } from '@interfaces/quizoot';
import type { Quiz, Question as QuizQuestion } from '@interfaces/quizoot.indexed';
import { useStore } from '@/store/store';
import { MutationTypes } from '@/store/types';
import { log } from '@/lib';
import { useFetch } from '@/lib/hooks';
import QuizPreview from '@/components/QuizPreview.vue';
import Question from '@/components/Question.vue';

const route = useRoute();
const store = useStore();

const quizQuestions: Ref<QuizQuestion[]> = ref([]);
const errorOccurred: Ref<boolean> = ref(false);
const isFetchingQuiz: ComputedRef<boolean> = computed(
    () => store.state.currentQuiz === null
);

onBeforeMount(() => {
    useFetch<Quiz>(`/api/quizzes/${route.params.id}`)
        .then((response) => {
            if (response.error.value) {
                errorOccurred.value = true;
                log(response.error.value);
            } else {
                store.commit(
                    MutationTypes.UPDATE_CURRENT_QUIZ,
                    response.data.value
                );

                for (const question of response.data.value?.questions) {
                    useFetch<QuizQuestion>(`/api/questions/${question.question_id}`)
                        .then((response) => {
                            if (response.error.value) {
                                log(response.error.value);
                            }
                            if (response.data.value) {
                                quizQuestions.value.push(response.data.value as QuizQuestion);
                            }
                        })
                        .catch((error) => {
                            log(error);
                        })
                }
            }
        })
        .catch((error) => {
            errorOccurred.value = true;
            log(error);
        });
});

const quiz: ComputedRef<Quiz | null> = computed(() => store.state.currentQuiz);

const currentQuestion: Ref<QuizQuestion | null> = ref(null);
const currentQuestionItem: Ref<Quizoot.QuestionItem | null> = ref(null);
const currentQuestionNumber: Ref<number> = ref(0);

const questionsFlow: ComputedRef = computed(() => {
    return {
        questionNumber:
            currentQuestionItem.value == null ? 0 : currentQuestionNumber.value,
        isFirstQuestion: currentQuestionItem.value?.prev_question_id == null,
        isLastQuestion: currentQuestionItem.value?.next_question_id == null,
    };
});

function getQuizQuestionOfId(id: Quizoot.Question['id']) {
    for (const question of quizQuestions.value) {
        if (question.id === id) {
            return question;
        }
    }
    return null;
}

function getFirstQuestionItem() {
    for (const question of quiz.value?.questions) {
        if (question.prev_question_id == null) {
            return question;
        }
    }
    return null;
}

function startQuiz() {
    currentQuestionItem.value = getFirstQuestionItem();
    if (currentQuestionItem.value) {
        currentQuestion.value = getQuizQuestionOfId(currentQuestionItem.value.question_id);
    }
    currentQuestionNumber.value = 1;
}

function quitQuiz() {
    currentQuestionItem.value = null;
    currentQuestion.value = null;
}

function goToNextQuestion() {
    if (currentQuestionItem.value?.next_question_id) {
        for (const question of quiz.value?.questions) {
            if (
                question.question_id === currentQuestionItem.value?.next_question_id
            ) {
                currentQuestionItem.value = question;
                currentQuestion.value = getQuizQuestionOfId(question.question_id)
                currentQuestionNumber.value++;
                return;
            }
        }
    }
    console.log(currentQuestion.value);
}

function goToPreviousQuestion() {
    if (currentQuestionItem.value?.prev_question_id) {
        for (const question of quiz.value?.questions) {
            if (
                question.question_id === currentQuestionItem.value?.prev_question_id
            ) {
                currentQuestionItem.value = question;
                currentQuestion.value = getQuizQuestionOfId(question.question_id)
                currentQuestionNumber.value--;
                return;
            }
        }
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
                v-if="currentQuestion != null"
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
            v-if="currentQuestion == null"
            :questionsCount="quizQuestions.length"
            :description="quiz.description"
            :authors="quiz.authors"
            :onStart="startQuiz"
        />
        <question
                v-else
                :question="currentQuestion"
                :questionsCount="quizQuestions.length"
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
