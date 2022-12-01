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
        Interactive Quiz <span>&#8226;</span>
        <span class="question-count">{{ props.questionsCount }}</span>
        Questions
        <p v-if="author">By {{ author.name }} {{ author.surname }}</p>
    </div>
    <div class="quiz-content">
        <p>{{ props.description }}</p>
    </div>
    <div class="btn-group">
        <button @click="onStart">Start the quiz <span>&#187;</span></button>
    </div>
</template>

<style>
.quiz-subtitle {
    margin-top: 5px;
}

.quiz-content {
    text-align: left;
    font-size: 1.2em;
}

.question-count {
    font-weight: 800;
    color: var(--palette-well-read);
}
</style>
