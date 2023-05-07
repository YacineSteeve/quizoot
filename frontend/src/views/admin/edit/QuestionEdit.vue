<script setup lang="ts">
import { ref, reactive, watch } from 'vue';
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

type SchemasName = 'base' | 'spec' | 'grading' | 'feedback';

type SchemasMap = Record<SchemasName, JsonSchema>;

interface StatesMap {
    base: Quizoot.Question;
    spec: Quizoot.Question['spec'];
    grading: Quizoot.Question['grading'];
    feedback: Quizoot.Question['grading']['feedback'];
}

const props = defineProps<QuestionEditProps>();

const route = useRoute();

const renderers = Object.freeze([...vanillaRenderers]);

const questionId = (route.params.id as string) || null;

const questionKindSelected: Ref<boolean> = ref(props.data.kind != undefined);

const questionKind: Ref = ref(
    questionKindSelected.value ? props.data.kind : null
);

const questionData: Ref<Quizoot.Question> = ref(props.data);

const questionSchemas: SchemasMap = {} as SchemasMap;

const schemasStates: StatesMap = questionKindSelected.value
    ? reactive({
          base: questionData.value,
          spec: questionData.value.spec,
          grading: questionData.value.grading,
          feedback: questionData.value.grading.feedback,
      })
    : reactive({
          base: {} as Quizoot.Question,
          spec: {} as Quizoot.Question['spec'],
          grading: {} as Quizoot.Question['grading'],
          feedback: {} as Quizoot.Question['grading']['feedback'],
      });

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

            const kind = getFormattedQuestionKind(value);
            const baseSchema = getSchema(kind.toLowerCase());

            if (isDefinition(baseSchema)) {
                questionSchemas.base = baseSchema;
                questionSchemas.spec = baseSchema.properties.spec;
                questionSchemas.grading = baseSchema.properties.grading;
                questionSchemas.feedback =
                    baseSchema.properties.grading.properties.feedback;
            }

            schemasStates.base.kind = kind;
        }
    },
    { immediate: true }
);

function getFormattedQuestionKind(kind: string): Quizoot.QuestionKind {
    if (!QuestionKind.enum.includes(kind as Quizoot.QuestionKind)) {
        throw new Error(`Question kind ${kind} is not valid.`);
    }

    if (kind === 'CHOICE_QUESTION') {
        if ('answer_id' in props.data.spec) {
            return 'SINGLE_CHOICE_QUESTION';
        } else {
            return 'MULTIPLE_CHOICES_QUESTION';
        }
    }

    return kind as Quizoot.QuestionKind;
}

function getRestoredQuestionKind(kind: Quizoot.QuestionKind): string {
    if (
        ['SINGLE_CHOICE_QUESTION', 'MULTIPLE_CHOICES_QUESTION'].includes(kind)
    ) {
        return 'CHOICE_QUESTION';
    }

    return kind;
}

function resolveRefs(
    schema: JsonSchema,
    definitionsMap: { [key: string]: JsonSchema }
) {
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

function chooseQuestionKind(kind: Quizoot.QuestionKind) {
    questionKind.value = kind;
    questionKindSelected.value = true;
}

function handleDataChange(key: SchemasName) {
    return (event: JsonFormsChangeEvent) => {
        schemasStates[key] = event.data;
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
    questionData.value = {
        ...schemasStates.base,
        // @ts-ignore
        kind: getRestoredQuestionKind(schemasStates.base.kind),
        spec: schemasStates.spec,
        grading: {
            ...schemasStates.grading,
            feedback: schemasStates.feedback,
        },
    };

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
            :onChange="handleDataChange(key as SchemasName)"
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
