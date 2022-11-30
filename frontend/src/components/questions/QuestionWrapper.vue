<script setup lang="ts">
import { computed, defineProps } from 'vue';

import type { Quizoot } from '@schemas/interface';

/** Import the different questions */
import CodeQuestion from './CodeQuestion.vue';
import ChoiceQuestion from './ChoiceQuestion.vue';
import TextQuestion from './TextQuestion.vue';
import UploadQuestion from './UploadQuestion.vue';

interface QuestionWrapperProps {
    question: Quizoot.Question;
}

const props = defineProps<QuestionWrapperProps>();

// TODO: write a generic factory that automatically finds
// the questions component.
function getQuestionComponent() {
    switch (props.question.kind) {
        case 'CHOICE_QUESTION':
            return ChoiceQuestion;
        case 'CODE_QUESTION':
            return CodeQuestion;
        case 'TEXT_QUESTION':
            return TextQuestion;
        case 'UPLOAD_QUESTION':
            return UploadQuestion;
        default:
            throw Error('Unknown Question');
    }
}

const componentId = computed(getQuestionComponent);
</script>
<template>
    <div class="progress-bar"></div>
    <div class="question">
        <component :is="componentId" />
    </div>
</template>
<style>
.quiz-container {
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: center;
    width: 65%;
    margin-left: 17.5%;
    margin-right: 17.5%;
    padding-bottom: 30px;
    min-height: 60vh;
}

.quiz-title {
    margin-bottom: 0;
}
</style>
