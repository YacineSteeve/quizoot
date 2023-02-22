<script setup lang="ts">
import { ref, computed } from 'vue';
import type { Ref, ComputedRef } from 'vue';
import { useRoute } from 'vue-router';
import type { Quizoot } from '@interfaces/quizoot';
import type { Quiz } from '@interfaces/quizoot.indexed';
import { log } from '@/lib';
import { useFetch } from '@/lib/hooks';
import QuizPreview from '@/components/QuizPreview.vue';
import Question from '@/components/Question.vue';
import QuestionsNavigation from '@/components/QuestionsNavigation.vue';
import FetchError from '@/components/FetchError.vue';
import Loader from '@/components/Loader.vue';

const route = useRoute();

const quiz: Ref<Quiz | null> = ref(null);
const errorOccurred: Ref<boolean> = ref(false);
const isFetchingQuiz: Ref<boolean> = ref(true);

useFetch<Quiz>(`/api/quizzes/${route.params.id}`)
    .then((response) => {
        if (response.error.value) {
            errorOccurred.value = true;
            log(response.error.value);
        } else {
            quiz.value = response.data.value;
        }
        isFetchingQuiz.value = false;
    })
    .catch((error) => {
        errorOccurred.value = true;
        isFetchingQuiz.value = false;
        log(error);
    });

const questionItems: ComputedRef<
    Record<Quizoot.QuestionItem['question_id'], Quizoot.QuestionItem>
> = computed(() => {
    const questionItems: Record<
        Quizoot.QuestionItem['question_id'],
        Quizoot.QuestionItem
    > = {};
    for (const questionItem of quiz.value?.questions || []) {
        questionItems[questionItem.question_id] = questionItem;
    }
    return questionItems;
});

const currentQuestionItem: Ref<Quizoot.QuestionItem | null> = ref(null);
const currentQuestionNumber: Ref<number> = ref(0);

function getFirstQuestionItem() {
    for (const question of quiz.value?.questions || []) {
        if (question.prev_question_id === null) {
            return question;
        }
    }
    return null;
}

function startQuiz() {
    currentQuestionItem.value = getFirstQuestionItem();
    currentQuestionNumber.value = 1;
}

function quitQuiz() {
    currentQuestionItem.value = null;
    currentQuestionNumber.value = 0;
}

function goToNextQuestion() {
    if (currentQuestionItem.value?.next_question_id) {
        currentQuestionItem.value =
            questionItems.value[currentQuestionItem.value.next_question_id];
        currentQuestionNumber.value++;
    }
}

function goToPreviousQuestion() {
    if (currentQuestionItem.value?.prev_question_id) {
        currentQuestionItem.value =
            questionItems.value[currentQuestionItem.value.prev_question_id];
        currentQuestionNumber.value--;
    }
}
</script>

<template>
    <FetchError v-if="errorOccurred" />
    <Loader v-else-if="isFetchingQuiz" />
    <div v-else class="quiz-container">
        <h1 class="quiz-title">
            <span
                v-if="currentQuestionItem != null"
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
            v-if="currentQuestionItem === null"
            :questionsCount="quiz.questions.length"
            :description="quiz.description"
            :authors="quiz.authors"
            :onStart="startQuiz"
        />
        <Suspense>
            <question
                v-if="currentQuestionItem != null"
                :questionId="currentQuestionItem.question_id"
                :questionsCount="quiz.questions.length"
                :questionNumber="currentQuestionNumber"
                :key="currentQuestionItem.question_id"
            >
            </question>
        </Suspense>
        <QuestionsNavigation
            v-if="currentQuestionItem != null"
            :isFirstQuestion="currentQuestionNumber === 1"
            :isLastQuestion="currentQuestionNumber === quiz.questions.length"
            :goToNextQuestion="goToNextQuestion"
            :goToPreviousQuestion="goToPreviousQuestion"
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
