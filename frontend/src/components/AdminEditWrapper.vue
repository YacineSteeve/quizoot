<script setup lang="ts">
interface AdminManageEditProps {
    element: 'quiz' | 'question';
    elementId: string | null;
    onCanceled: () => void;
    onSaved: () => void;
}

const props = defineProps<AdminManageEditProps>();
</script>

<template>
    <div class="admin-edit-wrapper-container">
        <h1 v-if="props.elementId === null">
            Create a new {{ props.element }}
        </h1>
        <h1 v-else>Edit {{ props.element }} # {{ props.elementId }}</h1>
        <hr />
        <slot></slot>
        <div class="buttons">
            <button @click.prevent="props.onCanceled">Cancel</button>
            <button @click.prevent="props.onSaved">Save</button>
        </div>
    </div>
</template>

<style scoped>
.admin-edit-wrapper-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1em;
}

h1 {
    width: 100%;
    text-align: left;
    margin-bottom: 0;
}

hr {
    width: 100%;
    margin-bottom: 1em;
}

.buttons {
    display: flex;
    justify-content: center;
    gap: 3em;
    margin-top: 2em;
}

.buttons button {
    color: #ffffff;
    cursor: pointer;
    font-size: 1em;
    font-weight: bold;
    padding: 0.5em 1em;
    border-radius: 0.25em;
    border: none;
}

.buttons button:first-child {
    background-color: var(--text-red);
}

.buttons button:first-child:hover {
    background-color: #8b0000cc;
}

.buttons button:last-child {
    background-color: var(--text-green);
}

.buttons button:last-child:hover {
    background-color: green;
}

@media only screen and (max-width: 600px) {
    h1,
    hr {
        width: 90%;
    }
}
</style>
