<script setup lang="ts">
import { computed, ref, watch } from 'vue';
import type { Ref } from 'vue';
import { useRoute } from 'vue-router';
import { JsonForms } from '@jsonforms/vue';
import { vanillaRenderers } from '@jsonforms/vue-vanilla';
import { useFetch } from '@/lib/hooks';
import type { Quizoot } from '@interfaces/quizoot';
// TODO: Fix relative paths
import CodeQuestionSchema from '../../../../../interfaces/schemas/code_question.json';
import MultipleChoicesQuestionSchema from '../../../../../interfaces/schemas/multiple_choices_question.json';
import SingleChoiceQuestionSchema from '../../../../../interfaces/schemas/text_question.json';
import TextQuestionSchema from '../../../../../interfaces/schemas/text_question.json';
import UploadQuestionSchema from '../../../../../interfaces/schemas/upload_question.json';
import FetchError from '@/components/FetchError.vue';
import Loader from '@/components/Loader.vue';

const route = useRoute();

const schemas: Record<string, typeof TextQuestionSchema> = {
    code_question: CodeQuestionSchema,
    multiple_choices_question: MultipleChoicesQuestionSchema,
    single_choice_question: SingleChoiceQuestionSchema,
    text_question: TextQuestionSchema,
    upload_question: UploadQuestionSchema,
};

const questionId = (route.params.id as string) || null;

const {
    data: questionData,
    error,
    isFetching,
} = questionId === null
    ? { data: ref({}), error: ref(null), isFetching: ref(false) }
    : useFetch<Quizoot.Question>(`/api/questions/${questionId}/`);

const questionKind = ref<string>(
    questionId === null ? (route.params.kind as string) : 'text_question'
);

watch(questionData, () => {
    questionKind.value = (
        questionData.value as Quizoot.Question
    ).kind.toLowerCase();
});

const questionSchema = computed(() => {
    console.log(questionKind.value);
    const schema = schemas[questionKind.value];

    schema.properties.id.readOnly = true;

    return schema;
});

const renderers = Object.freeze([...vanillaRenderers]);

const newQuizData: Ref<Quizoot.Question> = ref({} as Quizoot.Question);

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
        questionId === null
            ? { url: '/api/quizzes/', method: 'POST' }
            : { url: `/api/quizzes/${questionId}/`, method: 'PATCH' };

    const { error: saveError } = useFetch<Quizoot.Question>(saveParams.url, {
        method: saveParams.method,
        data: newQuizData.value, // TODO: Fix validation
    });

    if (saveError.value) {
        alert('An error occurred while saving the question.');
        return;
    }

    window.history.back();
};
</script>

<template>
    <FetchError v-if="error" />
    <Loader v-else-if="isFetching" />
    <div v-else>
        <h1 v-if="questionId === null">Create a new Question</h1>
        <h1 v-else>Edit Question {{ questionId }}</h1>
        <JsonForms
            :data="questionData"
            :schema="questionSchema"
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
