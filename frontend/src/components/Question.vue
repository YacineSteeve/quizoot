<script setup lang="ts">
import { computed, defineAsyncComponent, ref } from 'vue';
import type { ComputedRef, Ref } from 'vue';
import type { Quizoot } from '@interfaces/quizoot';
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

const QuestionSpec: ComputedRef = computed(() => {
    if (props.question.kind in components) {
        return components[props.question.kind];
    } else {
        throw Error(`Unknown QuestionKind "${props.question.kind}"`);
    }
});

const DIFFICULTY_COLOR_MAP: Record<Quizoot.Difficulty, string> = {
    EASY: 'green',
    MEDIUM: 'orange',
    HARD: 'var(--palette-well-read)',
};

const difficultyColor: ComputedRef = computed(
    () => DIFFICULTY_COLOR_MAP[props.question.difficulty]
);

const displayHint: Ref<boolean> = ref(false);

function toggleHint() {
    displayHint.value = !displayHint.value;
}

function goTo(s: 'next' | 'previous') {
    displayHint.value = false;
    switch (s) {
        case 'next':
            props.goToNextQuestion();
            break;
        case 'previous':
            props.goToPreviousQuestion();
            break;
        default:
            break;
    }
}
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

        <div class="question">
            <p>{{ props.question.question }}</p>
        </div>

        <keep-alive>
            <QuestionSpec :spec="props.question.spec" />
        </keep-alive>

        <div v-if="props.question.hint" class="question-hint">
            <div @click="toggleHint" class="hint-toggler">
                <font-awesome-icon
                    v-if="displayHint"
                    icon="fa-solid fa-caret-down"
                    size="lg"
                />
                <font-awesome-icon
                    v-else
                    icon="fa-solid fa-caret-right"
                    size="lg"
                />
                <p>Hint</p>
            </div>
            <div class="hint" :class="{ display: displayHint }">
                {{ props.question.hint }}
            </div>
        </div>

        <div class="navigation-button-group">
            <navigation-button
                v-if="!props.questionsFlow.isFirstQuestion"
                @click="goTo('previous')"
                backgroundColor="var(--palette-mobster)"
                chevronLeft
                class="previous-button button"
            >
                Previous
            </navigation-button>

            <navigation-button
                v-if="!props.questionsFlow.isLastQuestion"
                @click="goTo('next')"
                backgroundColor="var(--main-purple-lightened)"
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
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
    height: 100%;
}

.question-number h1 span {
    font-size: 0.7em;
}

.question-props {
    display: flex;
    justify-content: center;
    gap: 10px;
}

.question-props > * {
    width: fit-content;
}

.question-props #difficulty {
    text-align: right;
    flex: 1;
    letter-spacing: 1px;
    color: v-bind(difficultyColor);
    font-weight: 600;
}

.question-props #grading {
    text-align: left;
    flex: 1;
}

.question {
    width: 80%;
    margin-block: 30px;
}

.question p {
    width: 100%;
    text-align: left;
    font-size: 1.2em;
}

.question-hint {
    display: flex;
    flex-direction: column;
    gap: 5px;
    width: 80%;
    color: var(--main-purple-lightened);
    font-size: 1.1em;
    margin-bottom: 50px;
}

.question-hint .hint-toggler:hover {
    color: var(--main-purple);
}

.question-hint p {
    margin-block: 5px;
}

.hint-toggler {
    display: flex;
    align-items: center;
    cursor: pointer;
}

.hint-toggler p {
    margin-inline-start: 10px;
}

.hint {
    display: none;
    align-items: center;
    text-align: left;
    color: black;
    padding: 10px;
    /* margin-bottom: 50px; */
    border: 2px solid var(--main-purple-lightened);
    border-radius: 4px;
}

.display {
    display: block;
}

.navigation-button-group {
    display: flex;
    width: 80%;
    align-items: center;
    justify-content: center;
}

@media only screen and (max-width: 600px) {
    .question {
        text-align: left;
    }

    .question-hint {
        flex-direction: column;
        width: 90%;
    }

    .navigation-button-group {
        width: 100%;
    }
}

.navigation-button-group .button {
    min-width: 150px;
}

.navigation-button-group:has(.button:nth-child(2)) {
    justify-content: space-between;
}

.navigation-button-group:has(.previous-button) {
    justify-content: flex-start;
}

.navigation-button-group:has(.next-button) {
    justify-content: flex-end;
}
</style>
