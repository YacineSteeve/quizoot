<script setup lang="ts">
import { ref } from 'vue';
import type { Ref } from 'vue';
import { useRoute } from 'vue-router';
import { JsonForms } from '@jsonforms/vue';
import { vanillaRenderers } from '@jsonforms/vue-vanilla';
import { QuizSchema as quizSchema } from '@interfaces/schemas';
import type { Quizoot } from '@interfaces/quizoot';
import { useFetch } from '@/lib/hooks';

interface QuizEditProps {
    data: Quizoot.Quiz;
}

const props = defineProps<QuizEditProps>();

const route = useRoute();

const quizId = (route.params.id as string) || null;

const renderers = Object.freeze([...vanillaRenderers]);

quizSchema.properties.id.readOnly = true;

const newQuizData: Ref<Quizoot.Quiz> = ref({} as Quizoot.Quiz);

const onChange = (event) => {
    newQuizData.value = event.data;
};

const cancelEdit = () => {
    if (
        confirm(
            'Are you sure you want to cancel ? All unsaved changes will be lost.'
        )
    ) {
        window.history.back();
    }
};

const saveQuiz = () => {
    const saveParams =
        quizId === null
            ? { url: '/api/quizzes/', method: 'POST' }
            : { url: `/api/quizzes/${quizId}/`, method: 'PATCH' };

    const { error: saveError } = useFetch<Quizoot.Quiz>(saveParams.url, {
        method: saveParams.method,
        data: newQuizData.value, // TODO: Fix validation
    });

    if (saveError.value) {
        alert('An error occurred while saving the quiz.');
        return;
    }

    window.history.back();
};
</script>

<template>
    <div>
        <h1 v-if="quizId === null">Create a new Quiz</h1>
        <h1 v-else>Edit Quiz {{ quizId }}</h1>
        <JsonForms
            :data="props.data"
            :schema="quizSchema"
            :renderers="renderers"
            :onChange="onChange"
        />
        <div>
            <button @click.prevent="cancelEdit">Cancel</button>
            <button @click.prevent="saveQuiz">Save</button>
        </div>
    </div>
</template>

<style scoped></style>
