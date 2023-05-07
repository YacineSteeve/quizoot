<script setup lang="ts">
import { ref, watch } from 'vue';
import type { Ref } from 'vue';
import { useRoute } from 'vue-router';
import { vanillaRenderers } from '@jsonforms/vue-vanilla';
import { JsonForms } from '@jsonforms/vue';
import type { JsonFormsChangeEvent } from '@jsonforms/vue';
import type { JsonSchema } from '@jsonforms/core';
import { useFetch } from '@/lib/hooks';
import { snakeToPascal } from '@/lib/string-utils';
import type { Quizoot } from '@interfaces/quizoot';
import {
    QuestionKindSchema as QuestionKind,
    QuestionSchema,
} from '@interfaces/schemas';
import AdminEditWrapper from '@/components/AdminEditWrapper.vue';

interface QuestionEditProps {
    data: Quizoot.Question;
}

type SchemaDefinitionKey = keyof typeof QuestionSchema.definitions;

type SchemasMap = Record<string, JsonSchema>;

type StatesMap = Record<string, Ref>;

const props = defineProps<QuestionEditProps>();

const route = useRoute();

const renderers = Object.freeze([...vanillaRenderers]);

const questionId = (route.params.id as string) || null;

const questionKindSelected: Ref<boolean> = ref(props.data.kind != undefined);

const questionKind: Ref = ref(
    questionKindSelected.value ? props.data.kind : null
);

const questionData: Ref<Quizoot.Question> = ref(props.data);

const [questionSchemas, schemasStates]: [Ref<SchemasMap>, Ref<StatesMap>] = [
    ref({} as SchemasMap),
    ref({} as StatesMap),
];

const isDefinition = (
    schema: JsonSchema
): schema is typeof schema & { properties: any } => {
    return Object.prototype.hasOwnProperty.call(schema, 'properties');
};

watch(
    questionKind,
    (value) => {
        if (questionKindSelected.value) {
            questionData.value.kind = value;

            const formattedKind = getFormattedQuestionKind(value).toLowerCase();
            const baseSchema = getSchema(formattedKind);

            [questionSchemas.value, schemasStates.value] =
                getNestedSchemas(baseSchema);
        }
    },
    { immediate: true }
);

function initState(key: string, data: { [key: string]: any }, state: Ref) {
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
}

function initDataKey(key: string, value: any, data: { [key: string]: any }) {
    if (key in data) {
        data[key] = value;
    } else {
        for (const nestedKey in data) {
            if (typeof data[nestedKey] === 'object') {
                initDataKey(key, data[nestedKey], value);
            }
        }
    }
}

function getRebuiltQuestionData(statesMap: StatesMap): Quizoot.Question {
    const data = { ...statesMap['base'].value };

    data.kind = getRestoredQuestionKind(data.kind);

    for (const key in statesMap) {
        if (key !== 'base') {
            initDataKey(key, statesMap[key].value, data);
        }
    }

    return data as Quizoot.Question;
}

function getFormattedQuestionKind(kind: string): string {
    if (kind === 'CHOICE_QUESTION') {
        if ('answer_id' in props.data.spec) {
            return 'SINGLE_CHOICE_QUESTION';
        } else {
            return 'MULTIPLE_CHOICES_QUESTION';
        }
    }

    return kind;
}

function getRestoredQuestionKind(kind: string): string {
    if (
        ['SINGLE_CHOICE_QUESTION', 'MULTIPLE_CHOICES_QUESTION'].includes(kind)
    ) {
        return 'CHOICE_QUESTION';
    }

    return kind;
}

function resolveRefs(schema: JsonSchema, definitionsMap: SchemasMap) {
    if (schema.$ref) {
        const definition = schema.$ref.split('/').pop();

        if (definition) {
            schema = definitionsMap[definition];
        }
    }

    if (schema.properties) {
        for (const key in schema.properties) {
            schema.properties[key] = resolveRefs(
                schema.properties[key],
                definitionsMap
            );
        }
    }

    if (schema.items) {
        schema.items = resolveRefs(schema.items as JsonSchema, definitionsMap);
    }

    return schema;
}

function getSchema(kind: string): JsonSchema {
    const formattedKind = snakeToPascal(kind);
    const schema =
        QuestionSchema.definitions[
            `Quizoot.${formattedKind}` as SchemaDefinitionKey
        ];

    if (!schema) {
        throw new Error(`Schema for kind ${kind} not found.`);
    }

    if (isDefinition(schema)) {
        schema.properties.id.readOnly = true;

        schema.properties.spec =
            QuestionSchema.definitions[
                `Quizoot.${formattedKind}Spec` as SchemaDefinitionKey
            ];
    }

    resolveRefs(schema, QuestionSchema.definitions);

    return schema;
}

function flattenNestedProperties(schema: JsonSchema, outputMap: SchemasMap) {
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
}

function getNestedSchemas(baseSchema: JsonSchema): [SchemasMap, StatesMap] {
    const schemasMap = {} as SchemasMap;
    const statesMap = {} as StatesMap;

    schemasMap['base'] = { ...baseSchema } as JsonSchema;

    flattenNestedProperties(schemasMap['base'], schemasMap);

    // TODO: Cache the schemas map to avoid rebuilding it on every render

    for (const key in schemasMap) {
        statesMap[key] = ref({});
    }

    for (const key in schemasMap) {
        initState(key, props.data, statesMap[key]);
    }

    return [schemasMap, statesMap];
}

function chooseQuestionKind(kind: Quizoot.QuestionKind) {
    questionKind.value = kind;
    questionKindSelected.value = true;
}

function handleDataChange(key: string) {
    return (event: JsonFormsChangeEvent) => {
        schemasStates.value[key].value = event.data;
    };
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
    questionData.value = getRebuiltQuestionData(schemasStates.value);

    const saveParams =
        questionId === null
            ? { url: '/api/questions/', method: 'POST' }
            : { url: `/api/questions/${questionId}/`, method: 'PATCH' };

    const { error: saveError } = useFetch<Quizoot.Question>(saveParams.url, {
        method: saveParams.method,
        data: questionData.value,
    });

    if (saveError.value) {
        alert('An error occurred while saving the question.');
        return;
    }

    window.history.back();
}
</script>

<template>
    <admin-edit-wrapper
        element="question"
        :elementId="questionId"
        :onCanceled="cancelEdit"
        :onSaved="saveQuiz"
    >
        <div v-if="!questionKindSelected" class="choose-kind">
            <h2>Choose a question kind</h2>
            <button
                v-for="kind in QuestionKind.enum"
                :key="kind"
                @click="chooseQuestionKind(kind)"
            >
                {{ kind }}
            </button>
        </div>

        <JsonForms
            v-else
            v-for="([key, schema], index) in Object.entries(questionSchemas)"
            :key="index"
            :data="schemasStates[key]"
            :schema="schema"
            :renderers="renderers"
            :onChange="handleDataChange(key)"
        />
    </admin-edit-wrapper>
</template>

<style scoped>
.choose-kind {
    display: flex;
    flex-direction: column;
    gap: 1em;
}

.choose-kind button {
    cursor: pointer;
    color: #000000;
    font-weight: bold;
    padding: 0.5em;
    border-radius: 0.25em;
    border: none;
    width: fit-content;
    background-color: #ffffff;
}

.choose-kind button:hover {
    background-color: #000000;
    color: #ffffff;
}
</style>
