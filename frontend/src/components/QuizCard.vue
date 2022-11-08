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
        <div class="quiz-status" v-on:click="quiz.status = !quiz.status">
            <font-awesome-icon icon="fa-solid fa-check" color="#ffffff" size="l" v-if="quiz.status" />
        </div>
        <div class="quiz-details">
            <div class="quiz-title">
                <h2>{{ quiz.title }}</h2>
            </div>
            <div class="quiz-description">
                <p>{{ quiz.description }}</p>
            </div>
        </div>
        <div class="quiz-details-expand-icon">
            <font-awesome-icon icon="fa-solid fa-chevron-right" size="l" />
        </div>
    </div>
</template>

<style scoped>
.quiz-preview-container {
    display: flex;
    align-items: start;
    width: 75%;
    height: 16vh;
    margin-block: 3vh;
    border-radius: 10px;
    box-shadow: 0 5px 20px rgba(0, 0, 0, 0.5);
    background-color: #ffffff;
    transition: all 0.5s ease-out;
}

.quiz-preview-container:hover {
    transform: scale(1.05);
}

.quiz-preview-container .quiz-status,
.quiz-details-expand-icon {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 5%;
    margin-inline: 3%;
    margin-top: 5.5vh;
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
    justify-content: flex-end;
    align-items: stretch;
    text-align: left;
    width: 78%;
    height: 100%;
}

.quiz-preview-container .quiz-details>* {
    width: 100%;
    height: 8vh;
}

.quiz-preview-container .quiz-details .quiz-title {
    display: flex;
    justify-content: center;
    align-items: center;
}

.quiz-preview-container .quiz-details .quiz-title h2 {
    width: 100%;
    height: fit-content;
    margin-bottom: 1vh;
}

.quiz-preview-container .quiz-details .quiz-description p {
    margin-top: 1vh;
}

.quiz-preview-container .quiz-details>*>* {
    height: fit-content;
    text-overflow: ellipsis;
    white-space: nowrap;
    overflow: hidden;
}
</style>
