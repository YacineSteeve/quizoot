<script setup lang="ts">
import { computed, ref } from 'vue';
import type { ComputedRef, Ref } from 'vue';
import type { Quizoot } from '@interfaces/quizoot';

interface Specs {
    spec: Quizoot.UploadQuestion;
    filesList: Ref<File[]>;
}

interface HTMLInputEvent extends Event {
    target: HTMLInputElement & EventTarget;
}

const props = withDefaults(defineProps<Specs>(), {
    filesList: () => ref([]),
});

const isDragOver: Ref<boolean> = ref(false);

const dragDropAreaColor: ComputedRef = computed(() => {
    return isDragOver.value ? 'var(--palette-foam)' : 'white';
});

function removeFileFromList(fileIndex: number) {
    props.filesList.value.splice(fileIndex, 1);
}

function onDragOver(event: DragEvent) {
    event.preventDefault();
    isDragOver.value = true;
}

function onDragLeave(event: DragEvent) {
    event.preventDefault();
    isDragOver.value = false;
}

function onFileAdd(event: HTMLInputEvent | DragEvent) {
    event.preventDefault();
    const files =
        (event as HTMLInputEvent).target.files ||
        (event as DragEvent).dataTransfer?.files;
    if (files?.length) {
        for (const file of files) {
            if (props.filesList.value.includes(file)) {
                removeFileFromList(props.filesList.value.indexOf(file));
            }
            if (props.filesList.value.length < props.spec.max_files) { // TODO: Check file size too
                props.filesList.value.push(file);
            }
        }
        // TODO: Process the files in filesList as needed (maybe using a helper func defined in libs)
    }
    onDragLeave(event as DragEvent);
}
</script>

<template>
    <div class="upload-question-container">
        <div class="allowed-info">
            <div>
                Max file size: <b>{{ spec.max_size }}</b>
            </div>
            <div>
                Max number of files: <b>{{ spec.max_files }}</b>
            </div>
        </div>
        <div class="drag-drop-outer">
            <div class="inner">
                <input
                    @change="onFileAdd"
                    type="file"
                    multiple
                    id="file-input"
                />
                <label
                    @dragover="onDragOver"
                    @dragleave="onDragLeave"
                    @drop="onFileAdd"
                    title="Upload file"
                    for="file-input"
                >
                    <font-awesome-icon
                        icon="fa-solid fa-file-arrow-up"
                        color="var(--palette-mobster)"
                    />
                    <span
                        >Drag and drop or <u>click here</u> to upload your
                        files</span
                    >
                </label>
            </div>
        </div>
        <ul v-if="props.filesList.value.length" class="files-list">
            <li v-for="(file, index) in props.filesList.value" :key="index">
                <div class="file-name" :title="file.name">{{ file.name }}</div>
                <button
                    @click="removeFileFromList(index)"
                    class="remove-file-button"
                >
                    Remove
                </button>
            </li>
        </ul>
    </div>
</template>

<style scoped>
.upload-question-container {
    display: flex;
    flex-direction: column;
    gap: 20px;
    margin-block: 50px;
}

.upload-question-container > * {
    margin-inline: 50%;
    transform: translateX(-50%);
    width: 70%;
}

.upload-question-container .allowed-info {
    display: flex;
    justify-content: flex-start;
    font-size: 0.9em;
}

.upload-question-container .allowed-info div {
    width: 100%;
}

.upload-question-container .drag-drop-outer {
    height: 150px;
    padding: 6px;
    border-radius: 12px;
    border: 2px solid var(--palette-mobster);
    background-color: v-bind(dragDropAreaColor);
}

.upload-question-container .drag-drop-outer .inner {
    display: flex;
    align-items: center;
    justify-content: center;
    box-sizing: border-box;
    font-size: 0.9em;
    height: 100%;
    border-radius: 6px;
    border: 2px dashed var(--palette-mobster);
}

.upload-question-container .drag-drop-outer .inner input {
    display: none;
}

.upload-question-container .drag-drop-outer .inner label {
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    flex-direction: column;
    width: 100%;
    height: 100%;
}

.upload-question-container .files-list {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 0;
    margin-bottom: 0;
}

.upload-question-container .files-list li {
    display: flex;
    align-items: center;
    justify-content: space-between;
    width: 60%;
    max-width: 60%;
    padding-block: 5px;
    border-top: thin solid black;
}

@media only screen and (max-width: 600px) {
    .upload-question-container .drag-drop-outer {
        width: 90%;
    }

    .upload-question-container .files-list {
        width: 100%;
        padding: 0;
    }

    .upload-question-container .files-list li {
        width: 100%;
        max-width: 100%;
    }
}

.upload-question-container .files-list li:first-child {
    border: none;
}

.upload-question-container .files-list li .file-name {
    flex: 1;
    text-align: left;
    font-style: italic;
    font-size: 0.9em;
    text-overflow: ellipsis;
    white-space: nowrap;
    overflow: hidden;
}

.upload-question-container .files-list li .remove-file-button {
    cursor: pointer;
    font-size: 0.8em;
    color: white;
    height: 1.7em;
    margin-left: 10px;
    border-radius: 4px;
    border: none;
    box-shadow: 0 0 3px 1px dimgray;
    background-color: var(--palette-well-read);
}
</style>
