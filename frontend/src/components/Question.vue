<script setup lang="ts">
import { computed, defineProps, defineAsyncComponent } from 'vue';
import { pascalToSnake } from '@/lib/string-utils';
import type { Quizoot } from '@schemas/interface';

interface QuestionWrapperProps {
    question: Quizoot.Question;
}

const props = defineProps<QuestionWrapperProps>();

type Components = () => Promise<any>;
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

const componentId = computed(() => {
    if (props.question.kind in components) {
        return components[props.question.kind];
    }
    throw Error(`Unknown QuestionKind "${props.question.kind}"`);
});
</script>

<template>
    <div class="progress-bar"></div>
    <div class="question">
        <component :is="componentId" />
    </div>
</template>

<style>

</style>
