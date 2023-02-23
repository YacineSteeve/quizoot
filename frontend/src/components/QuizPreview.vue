<script setup lang="ts">
import type { Quizoot } from '@interfaces/quizoot';
import { computed } from 'vue';
import NavigationButton from '@/components/NavigationButton.vue';

interface QuizPreviewProps {
    questionsCount: number;
    description?: string;
    authors?: Quizoot.Author[];
    onStart: () => void;
}

const props = defineProps<QuizPreviewProps>();

// Get the first author (for now)
const author = computed(() => props.authors?.[0]);
</script>

<template>
    <div class="quiz-preview">
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
        <div class="quiz-footer">
            <div class="btn-group">
                <navigation-button
                    @click="onStart"
                    backgroundColor="var(--palette-cutty-sark)"
                    chevronRight
                >
                    Start the quiz
                </navigation-button>
            </div>
        </div>
    </div>
</template>

<style>
.quiz-preview {
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    margin-top: 5vh;
}

.quiz-subtitle p {
    font-style: italic;
}

.quiz-content {
    text-align: left;
    font-size: 1.2em;
    width: 90%;
}

.quiz-content p {
    font-size: 1.1em;
    font-weight: 400;
}

.question-count {
    font-weight: 800;
    color: var(--palette-well-read);
}

.quiz-footer {
    width: 90%;
}

.btn-group {
    display: flex;
    width: 100%;
    justify-content: flex-end;
    align-items: center;
}
</style>
