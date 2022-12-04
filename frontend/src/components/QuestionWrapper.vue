<script setup lang="ts">
import { computed, defineAsyncComponent } from 'vue';
import type { ComputedRef, Component } from 'vue';
import type { Quizoot } from '@schemas/interface';
import NavigationButton from '@/components/NavigationButton.vue';
import { pascalToSnake } from '@/lib/string-utils';


interface QuestionsFlow {
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

const props = defineProps<QuestionWrapperProps>();

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

const QuestionComponent: ComputedRef = computed(() => components[props.question.kind] as Component);
</script>

<template>
    <div class="progress-bar"></div>
    <div class="question-wrapper">
        <QuestionComponent/>
        <div class="navigation-button-group">
            <navigation-button
                    v-if="!props.questionsFlow.isFirstQuestion"
                    @click="goToPreviousQuestion"
                    backgroundColor="var(--palette-well-read)"
                    navigateTo="left"
                    class="previous-button button"
            >
                Previous
            </navigation-button>
            <navigation-button
                    v-if="!props.questionsFlow.isLastQuestion"
                    @click="goToNextQuestion"
                    backgroundColor="var(--palette-well-read)"
                    navigateTo="right"
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

.question-wrapper .navigation-button-group {
    display: flex;
    width: 100%;
    align-items: center;
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
