<script setup lang="ts">
import { ref } from 'vue';
import type { Ref } from 'vue';
import { useRouter } from 'vue-router';
import { useFetch } from '@/lib/hooks';
import type { Quizoot } from '@interfaces/quizoot';
import Quiz from '../../../interfaces/schemas/quiz.json';
import Question from '../../../interfaces/schemas/text_question.json';
import QuestionKind from '../../../interfaces/schemas/question_kind.json';
import FetchError from '@/components/FetchError.vue';
import Loader from '@/components/Loader.vue';

interface ManageProps {
    elements: 'Questions' | 'Quizzes';
}

const props = defineProps<ManageProps>();

const router = useRouter();

type ElementType = Quizoot.Question | Quizoot.Quiz;

const elementsName: string = props.elements.toLowerCase();

const elementObject = props.elements === 'Quizzes' ? Quiz : Question;

const properties = Object.keys(elementObject.properties);

const { data, error, isFetching } = useFetch(`/api/${elementsName}`);

const showQuestionKinds: Ref<boolean> = ref(false);

const chooseQuestionKind = () => {
    showQuestionKinds.value = !showQuestionKinds.value;
};

const editionRoutes = {
    create: (element: ElementType) => {
        return {
            path: `/admin/${elementsName}/edit`,
            query: {
                data: JSON.stringify(element),
            },
        };
    },
    update: (element: ElementType) => {
        return {
            path: `/admin/${elementsName}/edit/${element.id}`,
            query: {
                data: JSON.stringify(element),
            },
        };
    },
};

const editElement = (action: 'create' | 'update', element?: ElementType) => {
    router.push(editionRoutes[action](element || {}));
};

const deleteElement = (id: string) => {
    if (
        confirm(
            'Are you sure you want to delete this ? This action is irreversible.'
        )
    ) {
        const { error: deleteError } = useFetch(`/api/${elementsName}/${id}/`, {
            method: 'DELETE',
        });

        if (deleteError.value) {
            alert('An error occurred while deleting the element.');
            return;
        }

        window.location.reload();
    }
};
</script>

<template>
    <FetchError v-if="error" />
    <Loader v-else-if="isFetching" />
    <div v-else class="manage-container">
        <div class="header">
            <h2>{{ props.elements }} ({{ data.length }})</h2>
            <span v-if="props.elements === 'Quizzes'" class="create-quiz">
                <button @click="editElement('create')">Create new</button>
            </span>
            <div v-else class="create-question">
                <span @click="chooseQuestionKind">Create new</span>
                <!--
                    I found very more easier to choose the question kind before creating ui.

                    The other way is to create the question ui (without the part for the spec)
                    and then dynamically generate the corresponding spec ui when the user
                    choose the kind in the dropdown list (see QuestionEdit.vue).
                    -->
                <div v-if="showQuestionKinds">
                    <button
                        v-for="kind in QuestionKind.enum as string[]"
                        :key="kind"
                        @click="
                            editElement('create', { kind } as Quizoot.Question)
                        "
                    >
                        {{ kind }}
                    </button>
                </div>
            </div>
        </div>
        <hr />
        <div class="elements">
            <table>
                <thead>
                    <tr>
                        <th>N°</th>
                        <th v-for="key in properties" :key="key">
                            {{ key.toUpperCase() }}
                        </th>
                        <th>ACTIONS</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(element, index) in data" :key="element.id">
                        <td>{{ index + 1 }}</td>
                        <td v-for="key in properties" :key="key">
                            <slot :name="key" :value="element[key]">
                                <!--
                                By default, the slot will display the value of the property.
                                If the property is an array, it will display the array as a list.

                                If you want to display something else, you can use the slot:

                                <Manage elements="Element">
                                    <template #property-name="{value: <thePropertyValuePassedToTheSlot>}">
                                        Anything you want to display in the cell
                                    </template>
                                    <template #another-property-name>
                                        Anything you want to display in the cell
                                    </template>
                                    ...
                                </Manage>
                            -->
                                <div v-if="Array.isArray(element[key])">
                                    <ul>
                                        <li
                                            v-for="(item, index) in element[
                                                key
                                            ]"
                                            :key="index"
                                        >
                                            {{ item }}
                                        </li>
                                    </ul>
                                </div>
                                <div v-else>
                                    {{ element[key] }}
                                </div>
                            </slot>
                        </td>
                        <td class="edit-element">
                            <div>
                                <button @click="editElement('update', element)">
                                    <font-awesome-icon
                                        icon="fa-solid fa-pen-to-square"
                                    />
                                </button>
                                <button @click="deleteElement(element.id)">
                                    <font-awesome-icon
                                        icon="fa-solid fa-trash"
                                    />
                                </button>
                            </div>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<style scoped>
.manage-container {
    width: 100%;
    margin-inline: auto;
}

.header {
    display: flex;
    gap: 5em;
    justify-content: flex-start;
    align-items: center;
    width: 100%;
    margin-bottom: 0.5em;
}

h2 {
    font-size: 2em;
    font-weight: 600;
    text-align: left;
    margin-bottom: 1em;
    padding: 0;
}

.create-question {
    position: relative;
}

.create-quiz button,
.create-question span {
    color: #ffffff;
    font-weight: bold;
    background-color: var(--text-green);
    padding: 0.5em;
    border-radius: 0.25em;
}

.create-quiz button:hover,
.create-question span:hover {
    background-color: green;
    text-decoration: none;
}

.create-question div {
    position: absolute;
    top: -25%;
    left: 125%;
    display: flex;
    flex-direction: column;
    gap: 0.5em;
    padding: 5px;
    background-color: #ffffffaa;
}

.create-question div button {
    text-decoration: none;
    color: #000000;
    font-weight: bold;
    padding: 0.25em;
    border-radius: 0.25em;
    border: thin solid #000000;
    background-color: #ffffff;
}

.create-question div button:hover {
    background-color: #000000;
    color: #ffffff;
}

.elements {
    margin-block: 3em;
}

table {
    width: 100%;
    border-collapse: collapse;
    border: 4px double #000000;
}

th,
td {
    border: 1px solid #000000;
    padding: 0.5em;
}

th:not(:first-child),
td:not(:first-child) {
    min-width: 75px;
}

td.edit-element div {
    display: flex;
    flex-direction: column;
    gap: 1em;
    justify-content: center;
    align-items: center;
}

td.edit-element div button {
    text-decoration: none;
    color: #ffffff;
    padding: 0.5em;
    border-radius: 0.25em;
}

td.edit-element div button:first-child {
    background-color: #007bff;
}

td.edit-element div button:first-child:hover {
    background-color: #0069d9;
}

td.edit-element div button:last-child {
    background-color: #dc3545;
}

td.edit-element div button:last-child:hover {
    background-color: #c82333;
}

ul {
    padding: 0;
    text-align: left;
}

li {
    list-style: disc inside;
    word-break: break-all;
    margin-block: 0.5em;
}
</style>
