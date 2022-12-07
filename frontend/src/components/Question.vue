<script setup lang="ts">
import { computed, defineAsyncComponent } from 'vue';
import type { ComputedRef } from 'vue';
import type { Quizoot } from '@schemas/interface';
import NavigationButton from '@/components/NavigationButton.vue';
import { pascalToSnake } from '@/lib/string-utils';

interface QuestionsFlow {
    questionNumber: number;
    isFirstQuestion: boolean;
    isLastQuestion: boolean;
}

interface QuestionWrapperProps {
    question: Quizoot.Question;
    questionsFlow: QuestionsFlow;
    questionsCount: number;
    goToPreviousQuestion: () => void;
    goToNextQuestion: () => void;
}

type Components = Promise<any>;
type ComponentsMap = Record<Quizoot.QuestionKind, Components>;

function getComponents() {
    const files = import.meta.glob('@/components/questions/*.vue');
    const components: Record<string, Components> = {};

    for (const filepath in files) {
        const filename = filepath.match(/.*\/(.+)\.vue$/)?.[1];
        if (filename) {
            const kind = pascalToSnake(filename).toUpperCase();
            components[kind] = defineAsyncComponent(
                () => import(`@/components/questions/${filename}.vue`)
            );
        }
    }

    return components as ComponentsMap;
}

const components = getComponents();

const props = defineProps<QuestionWrapperProps>();

const QuestionComponent: ComputedRef = computed(() => {
    if (props.question.kind in components) {
        return components[props.question.kind];
    } else {
        throw Error(`Unknown QuestionKind "${props.question.kind}"`);
    }
});

const difficultiesColors: Record<Quizoot.Difficulty, string> = {
    EASY: 'green',
    MEDIUM: 'orange',
    HARD: 'red',
};

const questionDifficultyColor: ComputedRef = computed(
    () => difficultiesColors[props.question.difficulty]
);
</script>

<template>
    <div class="progress-bar"></div>
    <div class="question-wrapper">
        <div class="question-number">
            <h1>
                Question {{ props.questionsFlow.questionNumber }}
                <span> / {{ props.questionsCount }}</span>
            </h1>
        </div>
        <div class="question-props">
            <span id="difficulty">{{
                props.question.difficulty.toUpperCase()
            }}</span>
            <span>&#8226; </span>
            <span id="grading"
                >{{ props.question.grading.point_value }} pts</span
            >
        </div>
        <QuestionComponent />
        <div class="navigation-button-group">
            <navigation-button
                v-if="!props.questionsFlow.isFirstQuestion"
                @click="goToPreviousQuestion"
                backgroundColor="var(--palette-well-read)"
                chevronLeft
                class="previous-button button"
            >
                Previous
            </navigation-button>
            <navigation-button
                v-if="!props.questionsFlow.isLastQuestion"
                @click="goToNextQuestion"
                backgroundColor="var(--palette-well-read)"
                chevronRight
                class="next-button button"
            >
                Next
            </navigation-button>
        </div>
    </div>
</template>

<style scoped>
.question-wrapper {
    width: 100%;
    height: 100%;
}

.question-wrapper .question-number h1 span {
    font-size: 0.7em;
}

.question-wrapper .question-props {
    display: flex;
    justify-content: center;
    gap: 10px;
}

.question-wrapper .question-props > * {
    width: fit-content;
}

.question-wrapper .question-props #difficulty {
    text-align: right;
    flex: 1;
    letter-spacing: 1px;
    color: v-bind(questionDifficultyColor);
}

.question-wrapper .question-props #grading {
    text-align: left;
    flex: 1;
}

.question-wrapper .navigation-button-group {
    display: flex;
    width: 70%;
    align-items: center;
    margin-inline: 50%;
    transform: translateX(-50%);
}

@media only screen and (max-width: 600px) {
    .question-wrapper .navigation-button-group {
        width: 100%;
    }
}

.question-wrapper .navigation-button-group .button {
    min-width: 150px;
}

.question-wrapper .navigation-button-group:has(.button:nth-child(2)) {
    justify-content: space-between;
}

.question-wrapper .navigation-button-group:has(.previous-button) {
    justify-content: flex-start;
}

.question-wrapper .navigation-button-group:has(.next-button) {
    justify-content: flex-end;
}
</style>