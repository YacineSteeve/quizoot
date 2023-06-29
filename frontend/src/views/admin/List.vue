<script setup lang="ts">
import { useRoute, useRouter } from 'vue-router';
import { useFetch } from '@/lib/hooks';
import { capitalize } from '@/lib/string-utils';
import type { Quizoot } from '@interfaces/quizoot';
import FetchError from '@/components/FetchError.vue';
import Loader from '@/components/Loader.vue';

const route = useRoute();

const router = useRouter();

const elementsName: string = (route.params.elements as string).toLowerCase();

const properties =
    elementsName === 'questions'
        ? ['id', 'question', 'kind']
        : ['id', 'title', 'description', 'questions'];

const { data, error, isFetching } = useFetch<
    Quizoot.Question[] | Quizoot.Quiz[]
>(`/api/${elementsName}`);

function editElement(
    action: 'create' | 'update',
    element?: Quizoot.Question | Quizoot.Quiz
) {
    router.push({
        path:
            action === 'create'
                ? `/admin/${elementsName}/edit`
                : `/admin/${elementsName}/edit/${element?.id}`,
        query: {
            data: JSON.stringify(element || {}),
        },
    });
}

function deleteElement(id: string) {
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
}
</script>

<template>
    <FetchError v-if="error" />
    <Loader v-else-if="isFetching" />
    <div v-else class="admin-list-container">
        <div class="header">
            <h2>{{ capitalize(elementsName) }} ({{ data?.length }})</h2>
            <button class="create-element" @click="editElement('create')">
                Create new
            </button>
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
                            <div v-if="Array.isArray(element[key])">
                                <ul>
                                    <li
                                        v-for="(item, index) in element[key]"
                                        :key="index"
                                    >
                                        {{ item }}
                                    </li>
                                </ul>
                            </div>
                            <div v-else>
                                {{ element[key] }}
                            </div>
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
.admin-list-container {
    display: flex;
    flex-direction: column;
    align-items: center;
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

hr {
    width: 100%;
}

h2 {
    font-size: 2em;
    font-weight: 600;
    text-align: left;
    margin-bottom: 1em;
    padding: 0;
}

button.create-element {
    cursor: pointer;
    color: #ffffff;
    font-size: 1.1em;
    font-weight: bold;
    background-color: var(--text-green);
    padding: 0.5em;
    border-radius: 0.25em;
    border: none;
}

button.create-element:hover {
    background-color: green;
    text-decoration: none;
}

.elements {
    display: flex;
    flex-direction: column;
    justify-content: center;
    margin-block: 3em;
    overflow-x: auto;
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
    cursor: pointer;
    color: #ffffff;
    font-weight: bold;
    padding: 0.5em;
    border-radius: 0.25em;
    border: none;
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
    margin-block: 1em;
    min-width: max-content;
}

@media only screen and (max-width: 600px) {
    .header {
        gap: unset;
        justify-content: space-between;
        align-items: center;
        width: 90%;
        margin-bottom: 0;
    }

    hr,
    .elements {
        width: 90%;
        margin-top: 2em;
    }
}
</style>
