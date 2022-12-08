<script setup lang="ts">
import { computed, ref, defineAsyncComponent } from 'vue';
import type { ComputedRef, Ref } from 'vue';
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

const QuestionSpecComponent: ComputedRef = computed(() => {
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

const hintIsDisplayed: Ref<boolean> = ref(false);

function toggleHint() {
    hintIsDisplayed.value = !hintIsDisplayed.value;
}

function resetHint() {
    hintIsDisplayed.value = false;
}

const hintStyleProps: ComputedRef = computed(() => {
    return hintIsDisplayed.value
        ? {
              display: 'flex',
              hintButtonBgColor: 'var(--palette-spun-pearl)',
              hintAreaBgColor: 'var(--palette-spun-pearl)',
              hintAreaMargin: '40px',
          }
        : {
              display: 'none',
              hintButtonBgColor: 'var(--palette-mobster)',
              hintAreaBgColor: 'transparent',
              hintAreaMargin: '20px',
          };
});
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
        <QuestionSpecComponent :spec="props.question.spec" />
        <div v-if="props.question.hint" class="question-hint">
            <div @click="toggleHint" class="hint-button">
                <font-awesome-icon icon="fa-solid fa-question" size="lg" />
                <p>Hint</p>
            </div>
            <div class="hint">
                {{ props.question.hint }}
            </div>
        </div>
        <div class="navigation-button-group">
            <navigation-button
                v-if="!props.questionsFlow.isFirstQuestion"
                @click="
                    resetHint();
                    goToPreviousQuestion();
                "
                backgroundColor="var(--palette-well-read)"
                chevronLeft
                class="previous-button button"
            >
                Previous
            </navigation-button>
            <navigation-button
                v-if="!props.questionsFlow.isLastQuestion"
                @click="
                    resetHint();
                    goToNextQuestion();
                "
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

.question-wrapper .question {
    width: 100%;
    text-align: justify;
    margin-block: 30px;
}

.question-wrapper .question-hint {
    display: flex;
    gap: 30px;
    width: max-content;
    max-width: 100%;
    margin-inline: 50%;
    transform: translateX(-50%);
    margin-bottom: v-bind('hintStyleProps.hintAreaMargin');
    padding: 20px;
    border-radius: 8px;
    background-color: v-bind('hintStyleProps.hintAreaBgColor');
}

.question-wrapper .question-hint .hint-button {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: space-evenly;
    width: 1.7em;
    height: 1.7em;
    min-width: 1.7em;
    padding: 5px;
    border-radius: 8px;
    border: 2px solid var(--palette-mobster);
    color: var(--text-yellow);
    background-color: v-bind('hintStyleProps.hintButtonBgColor');
}

.question-wrapper .question-hint .hint-button p {
    margin: 0;
    font-size: 0.6em;
    font-weight: bold;
}

.question-wrapper .question-hint .hint-button:hover {
    cursor: pointer;
    background-color: var(--palette-mobster);
}

.question-wrapper .question-hint .hint {
    display: v-bind('hintStyleProps.display');
    align-items: center;
    text-align: left;
    color: white;
    padding: 10px;
    border-radius: 8px;
    background-color: var(--palette-mobster);
}

.question-wrapper .navigation-button-group {
    display: flex;
    width: 70%;
    align-items: center;
    margin-inline: 50%;
    transform: translateX(-50%);
}

@media only screen and (max-width: 600px) {
    .question-wrapper .question {
        text-align: left;
    }

    .question-wrapper .question-hint {
        flex-direction: column;
        width: 90%;
    }

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
