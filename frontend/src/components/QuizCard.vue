<script setup lang="ts">
import { useAttrs, reactive, computed } from 'vue';

const attrs = useAttrs();

const quiz = reactive({
    title: 'Basic Data Types ' + attrs['key'],
    description: 'Here we are going to exercise on Python basic data types.',
    status: [true, false][Math.floor(Math.random() * 2)],
});

const bgColor = computed(() => (quiz.status ? '#008000' : '#dfe2ec'));
</script>

<template>
    <div class="quiz-preview-container">
        <div class="quiz-status-container">
            <div class="quiz-status" v-on:click="quiz.status = !quiz.status">
                <font-awesome-icon icon="fa-solid fa-check" color="#ffffff" size="lg" v-if="quiz.status"/>
            </div>
        </div>
        <div class="quiz-details">
            <div class="quiz-title">
                <h2>{{ quiz.title }}</h2>
            </div>
            <div class="quiz-description">
                <p>{{ quiz.description }}</p>
            </div>
        </div>
        <div class="quiz-details-expand-icon-container">
            <div class="quiz-details-expand-icon">
                <font-awesome-icon icon="fa-solid fa-chevron-right" size="lg"/>
            </div>
        </div>
    </div>
</template>

<style scoped>
.quiz-preview-container {
    display: flex;
    align-items: start;
    width: 75%;
    min-width: 600px;
    height: 16vh;
    min-height: 110px;
    margin-block: 3vh;
    border-radius: 10px;
    box-shadow: 0 5px 20px rgba(0, 0, 0, 0.5);
    background-color: #ffffff;
    transition: all 0.5s ease-out;
}

.quiz-preview-container:hover {
    transform: scale(1.05);
    cursor: pointer;
}

.quiz-preview-container .quiz-status-container,
.quiz-preview-container .quiz-details-expand-icon-container {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 11%;
    height: 100%;
}

.quiz-preview-container .quiz-status,
.quiz-preview-container .quiz-details-expand-icon {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 50%;
    aspect-ratio: 1 / 1;
    transform: scale(1);
}

.quiz-preview-container .quiz-status {
    border-radius: 50%;
    background-color: v-bind(bgColor);
}

.quiz-preview-container .quiz-details {
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
        width: 85%;
        min-width: auto;
        height: 14vh;
        margin-block: 2vh;
    }

    .quiz-preview-container .quiz-status-container,
    .quiz-preview-container .quiz-details-expand-icon-container {
        width: 14%;
    }

    .quiz-preview-container .quiz-details {
        width: 72%;
    }
}

.quiz-preview-container .quiz-details>* {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 35%;
}

.quiz-preview-container .quiz-details>*>* {
    width: 100%;
    height: fit-content;
    margin: 0;
    text-overflow: ellipsis;
    white-space: nowrap;
    overflow: hidden;
}
</style>
