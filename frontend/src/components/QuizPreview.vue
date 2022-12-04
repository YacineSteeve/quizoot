<script setup lang="ts">
import type { Quizoot } from '@schemas/interface';
import { defineProps, computed } from 'vue';

interface QuizPreviewProps {
    questionsCount: number;
    description: string;
    authors?: Quizoot.Author[];
    onStart: () => void;
}

const props = defineProps<QuizPreviewProps>();

// Get the first author (for now)
const author = computed(() => props.authors?.[0]);
</script>

<template>
    <div class="quiz-subtitle">
        <p v-if="author">by {{ author.name }} {{ author.surname }}</p>
        <span class="question-count">{{ props.questionsCount }}</span>
        Questions
    </div>
    <br/>
    <div class="quiz-content">
        <p>{{ props.description }}</p>
    </div>
    <br/>
    <div class="btn-group">
        <button @click="onStart">Start the quiz <span>&#187;</span></button>
    </div>
</template>

<style>
.quiz-subtitle {
    margin-top: 5px;
}

.quiz-subtitle p {
    font-style: italic;
}

.quiz-content {
    text-align: left;
    font-size: 1.2em;
    margin-inline: 10%;
}

.question-count {
    font-weight: 800;
    color: var(--palette-well-read);
}
</style>
