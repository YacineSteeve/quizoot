<script setup lang="ts">
import { computed, defineAsyncComponent, ref } from 'vue';
import type { ComputedRef, Ref } from 'vue';
import type { Quizoot } from '@interfaces/quizoot';
import { useFetch } from '@/lib/hooks';
import { pascalToSnake } from '@/lib/string-utils';
import FetchError from '@/components/FetchError.vue';
import Loader from '@/components/Loader.vue';

interface QuestionWrapperProps {
    id: Quizoot.Question['id'];
    rank: number;
    totalQuestions: number;
}

// Use any instead of Promise<object> so that we can use AyncComponent in the template.
// See https://github.com/vuejs/vue-class-component/issues/323
type Component = any;
type ComponentsMap = Record<Quizoot.QuestionKind, Component>;

function getComponents() {
    const files = import.meta.glob('@/components/questions/*.vue');
    const components: Record<string, Component> = {};

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

const {
    data: question,
    error: errorOccurred,
    isFetching: isFetchingQuestion,
} = await useFetch<Quizoot.Question>(`/api/questions/${props.id}`);

const QuestionSpec: ComputedRef<Component> = computed(() => {
    if (question.value?.kind && question.value?.kind in components) {
        return components[question.value?.kind as Quizoot.QuestionKind];
    } else {
        throw Error(`Unknown QuestionKind "${question.value?.kind}"`);
    }
});

const DIFFICULTY_COLOR_MAP: Record<Quizoot.Difficulty, string> = {
    EASY: 'green',
    MEDIUM: 'orange',
    HARD: 'var(--palette-well-read)',
};

const difficultyColor: ComputedRef = computed(
    () => DIFFICULTY_COLOR_MAP[question.value?.difficulty as Quizoot.Difficulty]
);

const displayHint: Ref<boolean> = ref(false);

function toggleHint() {
    displayHint.value = !displayHint.value;
}
</script>

<template>
    <div class="progress-bar"></div>
    <FetchError v-if="errorOccurred" />
    <Loader v-else-if="isFetchingQuestion" />
    <div v-else class="question-wrapper">
        <div class="question-number">
            <h1>
                Question {{ props.rank }}
                <span> / {{ props.totalQuestions }}</span>
            </h1>
        </div>

        <div class="question-props">
            <span id="difficulty">{{
                question?.difficulty.toUpperCase()
            }}</span>
            <span>&#8226; </span>
            <span id="grading">{{ question?.grading.point_value }} pts</span>
        </div>

        <div class="question">
            <p>{{ question?.question }}</p>
        </div>

        <keep-alive>
            <QuestionSpec :spec="question?.spec" />
        </keep-alive>

        <div v-if="question?.hint" class="question-hint">
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
                {{ question.hint }}
            </div>
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
    border: 2px solid var(--main-purple-lightened);
    border-radius: 4px;
}

.display {
    display: block;
}

@media only screen and (max-width: 600px) {
    .question {
        text-align: left;
    }

    .question-hint {
        flex-direction: column;
        width: 90%;
    }
}
</style>
