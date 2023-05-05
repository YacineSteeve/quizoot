<script setup lang="ts">
import { ref } from 'vue';
import type { Ref } from 'vue';
import { useRoute } from 'vue-router';
import { JsonForms } from '@jsonforms/vue';
import type { JsonSchema } from '@jsonforms/core';
import { vanillaRenderers } from '@jsonforms/vue-vanilla';
import { useFetch } from '@/lib/hooks';
import { snakeToPascal } from '@/lib/string-utils';
import type { Quizoot } from '@interfaces/quizoot';
import QuestionSchema from '../../../../../interfaces/schemas/question.json'; // TODO: Fix relative paths

/*
    This seems to be the less maintainable way to do this 🤮💔
    but it's the only way I found to make it work a bit.
 */

interface QuestionEditProps {
    data: Quizoot.Question;
}

type SchemasMap = Record<string, JsonSchema>;

type StatesMap = Record<string, Ref>;

const props = defineProps<QuestionEditProps>();

const route = useRoute();

const renderers = Object.freeze([...vanillaRenderers]);

const initState = (key: string, data: object, state: Ref) => {
    if (key === 'base') {
        state.value = data;
        state.value.kind = getFormattedQuestionKind(state.value.kind);
    } else if (key in data) {
        state.value = data[key];
    } else {
        for (const nestedKey in data) {
            if (typeof data[nestedKey] === 'object') {
                initState(key, data[nestedKey], state);
            }
        }
    }
};

const initDataKey = (key: string, value: any, data: object) => {
    if (key in data) {
        data[key] = value;
    } else {
        for (const nestedKey in data) {
            if (typeof data[nestedKey] === 'object') {
                initDataKey(key, data[nestedKey], value);
            }
        }
    }
};

const getRebuiltQuestionData = (statesMap: StatesMap): Quizoot.Question => {
    const data = { ...statesMap['base'].value };

    data.kind = getRestoredQuestionKind(data.kind);

    for (const key in statesMap) {
        if (key !== 'base') {
            initDataKey(key, statesMap[key].value, data);
        }
    }

    return data as Quizoot.Question;
};

const getFormattedQuestionKind = (kind: string): string => {
    if (kind === 'CHOICE_QUESTION') {
        if ('answer_id' in props.data.spec) {
            return 'SINGLE_CHOICE_QUESTION';
        } else {
            return 'MULTIPLE_CHOICES_QUESTION';
        }
    }

    return kind.toLowerCase();
};

const getRestoredQuestionKind = (kind: string): string => {
    if (
        ['SINGLE_CHOICE_QUESTION', 'MULTIPLE_CHOICES_QUESTION'].includes(kind)
    ) {
        return 'CHOICE_QUESTION';
    }

    return kind;
};

const resolveRefsOfProperties = (
    schema: JsonSchema,
    definitionsMap: SchemasMap
) => {
    if (schema.$ref) {
        const definition = schema.$ref.split('/').pop();

        if (definition) {
            schema = definitionsMap[definition];
        }
    }

    if (schema.properties) {
        for (const key in schema.properties) {
            schema.properties[key] = resolveRefsOfProperties(
                schema.properties[key],
                definitionsMap
            );
        }
    }

    if (schema.items) {
        schema.items = resolveRefsOfProperties(
            schema.items as JsonSchema,
            definitionsMap
        );
    }

    return schema;
};

const getSchema = (kind: string): JsonSchema => {
    const formattedKind = snakeToPascal(kind);
    const schema = QuestionSchema.definitions[`Quizoot.${formattedKind}`];

    if (!schema) {
        throw new Error(`Schema for kind ${kind} not found.`);
    }

    schema.properties.id.readOnly = true;

    schema.properties.spec =
        QuestionSchema.definitions[`Quizoot.${formattedKind}Spec`];

    resolveRefsOfProperties(schema, QuestionSchema.definitions);

    return schema;
};

const flattenNestedProperties = (schema: JsonSchema, outputMap: SchemasMap) => {
    if (schema.properties) {
        for (const key in schema.properties) {
            if (schema.properties[key].properties) {
                outputMap[key] = schema.properties[key];

                flattenNestedProperties(schema.properties[key], outputMap);
            } else {
                flattenNestedProperties(schema.properties[key], outputMap);
            }
        }
    }
};

const getNestedSchemas = (baseSchema: JsonSchema): [SchemasMap, StatesMap] => {
    const schemasMap = {} as SchemasMap;
    const statesMap = {} as StatesMap;

    schemasMap['base'] = { ...baseSchema } as JsonSchema;

    flattenNestedProperties(schemasMap['base'], schemasMap);

    for (const key in schemasMap) {
        statesMap[key] = ref({});
    }

    for (const key in schemasMap) {
        initState(key, props.data, statesMap[key]);
    }

    return [schemasMap, statesMap];
};

const questionId = (route.params.id as string) || null;

const questionKind = getFormattedQuestionKind(props.data.kind).toLowerCase();

const baseQuestionSchema = getSchema(questionKind);

const [questionSchemas, schemasStates] = getNestedSchemas(baseQuestionSchema);

const newQuizData: Ref<Quizoot.Question> = ref({} as Quizoot.Question);

const handleChange = (key: string) => (event) => {
    schemasStates[key].value = event.data;
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
    newQuizData.value = getRebuiltQuestionData(schemasStates);

    const saveParams =
        questionId === null
            ? { url: '/api/questions/', method: 'POST' }
            : { url: `/api/questions/${questionId}/`, method: 'PATCH' };

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
    <div>
        <h1 v-if="questionId === null">Create a new Question</h1>
        <h1 v-else>Edit Question {{ questionId }}</h1>
        <JsonForms
            v-for="([key, schema], index) in Object.entries(questionSchemas)"
            :key="index"
            :data="schemasStates[key]"
            :schema="schema"
            :renderers="renderers"
            :onChange="handleChange(key)"
        />
        <div>
            <button @click.prevent="cancelEdit">Cancel</button>
            <button @click.prevent="saveQuiz">Save</button>
        </div>
    </div>
</template>

<style scoped></style>
