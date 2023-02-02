<script setup lang="ts">
import { ref, computed } from 'vue';
import type { Quizoot } from '@interfaces/quizoot';

interface QuizCardProps {
    title: Quizoot.Quiz['title'];
    description: Quizoot.Quiz['description'];
}

const props = defineProps<QuizCardProps>();

const status = ref(true);

const bgColor = computed(() => (status ? '#008000' : '#dfe2ec'));
</script>

<template>
    <div class="quiz-preview-container">
        <div class="quiz-status-container">
            <div class="quiz-status" v-on:click="status = !status">
                <font-awesome-icon
                    icon="fa-solid fa-check"
                    color="#ffffff"
                    v-if="status"
                />
            </div>
        </div>
        <div class="quiz-details">
            <div class="quiz-title">
                <h2>{{ props.title }}</h2>
            </div>
            <div class="quiz-description">
                <p>{{ props.description }}</p>
            </div>
        </div>
        <div class="quiz-details-expand-icon-container">
            <div class="quiz-details-expand-icon">
                <font-awesome-icon icon="fa-solid fa-chevron-right" size="lg" />
            </div>
        </div>
    </div>
</template>

<style scoped>
.quiz-preview-container {
    display: flex;
    width: 75%;
    min-width: 600px;
    height: 16vh;
    min-height: 110px;
    margin-block: 3vh;
    margin-inline: auto;
    border-radius: 10px;
    box-shadow: 0 5px 20px rgba(0, 0, 0, 0.5);
    background-color: #ffffff;
    transition: all 0.5s ease-out;
}

.quiz-preview-container:hover {
    transform: scale(1.05);
    cursor: pointer;
}

.quiz-status-container,
.quiz-details-expand-icon-container {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 11%;
    height: 100%;
}

.quiz-status,
.quiz-details-expand-icon {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 50%;
    aspect-ratio: 1 / 1;
    transform: scale(1);
}

.quiz-status {
    border-radius: 50%;
    background-color: v-bind(bgColor);
}

.quiz-status > * {
    width: 80%;
}

.quiz-details {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: stretch;
    text-align: left;
    width: 78%;
    height: 100%;
}

@media only screen and (max-width: 600px) {
    .quiz-preview-container {
        width: 85vw;
        min-width: unset;
        height: 14vh;
        margin-block: 2vh;
    }

    .quiz-status-container,
    .quiz-details-expand-icon-container {
        width: 14%;
    }

    .quiz-details {
        width: 72%;
    }
}

.quiz-details > * {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 35%;
}

.quiz-details > * > * {
    width: 100%;
    height: fit-content;
    margin: 0;
    text-overflow: ellipsis;
    white-space: nowrap;
    overflow: hidden;
}
</style>
