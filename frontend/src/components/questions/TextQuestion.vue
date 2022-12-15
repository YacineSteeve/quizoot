<script setup lang="ts">
import { ref, computed } from 'vue';
import type { Quizoot } from '@interfaces/quizoot';
interface TextQuestionProps {
    spec: Quizoot.TextQuestion;
}
const props = defineProps<TextQuestionProps>();
const answer = ref('');
const placeholder = computed(
    () => props.spec.placeholder ?? 'Type your answer here...'
);
</script>

<template>
    <div class="text-question">
        <!-- TODO: add rows in spec as optional field -->
        <textarea
            :placeholder="placeholder"
            rows="8"
            v-model="answer"
        ></textarea>
    </div>
</template>

<style scoped>
.text-question {
    width: 80%;
    text-align: center;
}
textarea {
    width: 100%;
    border-radius: 5px;
    border: 2px solid var(--palette-mobster);
    padding: 5px;
    margin-bottom: 50px;
    font-size: 1.1em;
}
</style>
