<script setup lang="ts">
import { computed, ref } from 'vue';
import type { Ref } from 'vue';
import { useRoute } from 'vue-router';
import { JsonForms } from '@jsonforms/vue';
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

const props = defineProps<QuestionEditProps>();

const route = useRoute();

const renderers = Object.freeze([...vanillaRenderers]);

const questionId = (route.params.id as string) || null;

const questionKind = props.data.kind?.toLowerCase() || 'text_question';

const fillRefsOfProperties = (schema, definitionsMap) => {
    if (schema.$ref) {
        const definition = schema.$ref.split('/').pop();

        if (definition) {
            schema = definitionsMap[definition];
        }
    }

    if (schema.properties) {
        for (const key in schema.properties) {
            schema.properties[key] = fillRefsOfProperties(
                schema.properties[key],
                definitionsMap
            );
        }
    }

    if (schema.items) {
        schema.items = fillRefsOfProperties(schema.items, definitionsMap);
    }

    return schema;
};

const getSchema = (kind: string): object => {
    const formattedKind = snakeToPascal(kind);
    const schema = QuestionSchema.definitions[`Quizoot.${formattedKind}`];

    if (!schema) {
        throw new Error(`Schema for kind ${kind} not found.`);
    }

    schema.properties.id.readOnly = true;

    schema.properties.spec =
        QuestionSchema.definitions[`Quizoot.${formattedKind}Spec`];

    /*
        -------------------------------------------------------------
        I am doing these next three lines manually because of a bug
        in the "fillRefsOfProperties" function.

        Otherwise, I would have just done:

        fillRefsOfProperties(schema, QuestionSchema.definitions);
     */
    schema.properties.grading = QuestionSchema.definitions[`Quizoot.Grading`];

    schema.properties.grading.properties.feedback =
        QuestionSchema.definitions[`Quizoot.Feedback`];

    schema.properties.difficulty =
        QuestionSchema.definitions[`Quizoot.Difficulty`];

    //  -------------------------------------------------------------

    fillRefsOfProperties(schema.properties.spec, QuestionSchema.definitions);

    return schema;
};

const flattenNestedProperties = (schema, outputMap) => {
    if (schema.properties) {
        for (const key in schema.properties) {
            if (schema.properties[key].properties) {
                outputMap[key] = schema.properties[key];

                flattenNestedProperties(schema.properties[key], outputMap);

                delete schema.properties[key];
            } else {
                flattenNestedProperties(schema.properties[key], outputMap);
            }
        }
    }
};

const getRequiredSchemas = () => {
    const schemasMap = {};
    let kind = questionKind;

    if (kind === 'choice_question') {
        if ('answer_id' in props.data.spec) {
            kind = 'single_choice_question';
        } else {
            kind = 'multiple_choices_question';
        }
    }

    const baseSchema = getSchema(kind);

    schemasMap['base'] = baseSchema;

    flattenNestedProperties({ ...baseSchema }, schemasMap);

    // TODO: Generate states for each schema

    return Object.values(schemasMap);
};

const questionSchemas = computed(() => getRequiredSchemas());

const newQuizData: Ref<Quizoot.Question> = ref({} as Quizoot.Question);

const handleChange = (index: number) => (event) => {
    // TODO: Combine correctly the data of all schemas into one object
    // newQuizData.value = { ...event.data };
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
    <div>
        <h1 v-if="questionId === null">Create a new Question</h1>
        <h1 v-else>Edit Question {{ questionId }}</h1>
        <JsonForms
            v-for="(schema, index) in questionSchemas"
            :key="index"
            :data="{}"
            :schema="schema"
            :renderers="renderers"
        />
        <!-- :onChange="handleChange(index)" -->
        <div>
            <button @click.prevent="cancelEdit">Cancel</button>
            <button @click.prevent="saveQuiz">Save</button>
        </div>
    </div>
</template>

<style scoped></style>
