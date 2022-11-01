<script setup lang="ts">
    const quiz = {
        title: 'Basic Data Types',
        description: 'Here we are going to blablabla',
        status: false
    };
</script>

<template>
    <div class="quiz-preview-container">
        <div class="quiz-status"></div>
        <div class="quiz-details">
            <div class="quiz-title">
                <h2>{{ quiz.title }}</h2>
            </div>
            <div class="quiz-description">
                <p>{{ quiz.description }}</p>
            </div>
        </div>
        <div class="quiz-details-expand-icon">
            <p>&#8964;</p>
        </div>
    </div>
</template>

<style scoped>
.quiz-preview-container {
    display: flex;
    align-items: start;
    width: 75%;
    height: fit-content;
    min-height: 16vh;
    margin-block: 5vh;
    border-radius: 10px;
    box-shadow: 0 5px 20px rgba(0, 0, 0, 0.5);
}

.quiz-preview-container .quiz-status {
    width: 5vh;
    margin-inline: 3%;
    margin-top: 5.5vh;
    aspect-ratio: 1 / 1;
    transform: scale(1);
    border-radius: 50%;
    background-color: grey;
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

.quiz-preview-container .quiz-details > * {
    width: 100%;
    height: fit-content;
    min-height: 8vh;
}

.quiz-preview-container .quiz-details .quiz-title {
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    word-wrap: break-word;
}

.quiz-preview-container .quiz-details .quiz-title h2 {
    height: fit-content;
    margin-bottom: 1vh;
}

.quiz-preview-container .quiz-details .quiz-description {
}

.quiz-preview-container .quiz-details .quiz-description p {
    height: fit-content;
    margin-top: 1vh;
    text-overflow: ellipsis;
}

.quiz-preview-container .quiz-details-expand-icon {
    display: flex;
    justify-content: center;
    align-items: center;
    font-weight: bold;
    font-size: 2em;
    width: 11%;
}
</style>
