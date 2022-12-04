<script setup lang="ts">
import type { Quizoot } from '@schemas/interface';
import { computed } from 'vue';
import NavigationButton from "@/components/NavigationButton.vue";

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
    <br />
    <div class="quiz-content">
        <p>{{ props.description }}</p>
    </div>
    <br />
    <div class="btn-group">
        <navigation-button
                @click="onStart"
                backgroundColor="var(--palette-cutty-sark)"
                navigateTo="right">
            Start the quiz
        </navigation-button>
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
