<script setup lang="ts">
import { ref } from 'vue';
import type { Ref } from 'vue';
import { useRoute } from 'vue-router';
import { vanillaRenderers } from '@jsonforms/vue-vanilla';
import { JsonForms } from '@jsonforms/vue';
import type { JsonFormsChangeEvent } from '@jsonforms/vue';
import { QuizSchema as quizSchema } from '@interfaces/schemas';
import type { Quizoot } from '@interfaces/quizoot';
import { useFetch } from '@/lib/hooks';
import AdminEditWrapper from '@/components/AdminEditWrapper.vue';

interface QuizEditProps {
    data: Quizoot.Quiz;
}

const props = defineProps<QuizEditProps>();

const route = useRoute();

const renderers = Object.freeze([...vanillaRenderers]);

const quizId = (route.params.id as string) || null;

const quizData: Ref<Quizoot.Quiz> = ref(props.data);

type QuizSchemaId = typeof quizSchema.properties.id & { readOnly: boolean };

(quizSchema.properties.id as QuizSchemaId).readOnly = true;

function handleDataChange(event: JsonFormsChangeEvent) {
    quizData.value = event.data;
}

function cancelEdit() {
    if (
        confirm(
            'Are you sure you want to cancel ? All unsaved changes will be lost.'
        )
    ) {
        window.history.back();
    }
}

function saveQuiz() {
    const saveParams =
        quizId === null
            ? { url: '/api/quizzes/', method: 'POST' }
            : { url: `/api/quizzes/${quizId}/`, method: 'PATCH' };

    const { error: saveError } = useFetch<Quizoot.Quiz>(saveParams.url, {
        method: saveParams.method,
        data: quizData.value,
    });

    if (saveError.value) {
        alert('An error occurred while saving the quiz.');
        return;
    }

    window.history.back();
}
</script>

<template>
    <admin-edit-wrapper
        element="quiz"
        :elementId="quizId"
        :onCanceled="cancelEdit"
        :onSaved="saveQuiz"
    >
        <JsonForms
            :data="quizData"
            :schema="quizSchema"
            :renderers="renderers"
            :onChange="handleDataChange"
        />
    </admin-edit-wrapper>
</template>

<style scoped></style>
