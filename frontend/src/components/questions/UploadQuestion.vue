<script setup lang="ts">
import { ref } from 'vue';
import type { Ref } from 'vue';
import type { Quizoot } from '@interfaces/quizoot';

interface UploadQuestionProps {
    spec: Quizoot.UploadQuestionSpec;
}

interface HTMLInputEvent extends Event {
    target: HTMLInputElement & EventTarget;
}

const props = defineProps<UploadQuestionProps>();

const files: Ref<File[]> = ref([]);

const isDragOver = ref(false);

const isDragEvent = (event: HTMLInputEvent | DragEvent): event is DragEvent =>
    'dataTransfer' in event;

const getFileList = (event: HTMLInputEvent | DragEvent) => {
    if (isDragEvent(event)) {
        return event.dataTransfer?.files;
    }
    return event.target.files;
};

function addFiles(fileList: FileList) {
    for (const file of fileList) {
        if (files.value.includes(file)) {
            removeFile(files.value.indexOf(file));
        }
        if (files.value.length < props.spec.max_files) {
            // TODO: Check file size too
            files.value.push(file);
        }
    }
    // TODO: Process the files as needed (maybe using a helper func defined in libs)
}

function removeFile(fileIndex: number) {
    files.value.splice(fileIndex, 1);
}

function onDragOver(event: DragEvent) {
    event.preventDefault();
    isDragOver.value = true;
}

function onDragLeave(event: DragEvent) {
    event.preventDefault();
    isDragOver.value = false;
}

function onFileAdd(event: Event) {
    event.preventDefault();
    const fileList = getFileList(event as HTMLInputEvent | DragEvent);
    if (fileList) {
        addFiles(fileList);
    }
}

function onFileDrop(event: DragEvent) {
    onFileAdd(event);
    onDragLeave(event);
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
        <div
            class="drag-drop-outer"
            :class="{ dragover: isDragOver, dragleave: !isDragOver }"
        >
            <div class="drag-drop-inner">
                <input
                    @change="onFileAdd"
                    type="file"
                    multiple
                    id="file-input"
                />
                <label
                    @dragover="onDragOver"
                    @dragleave="onDragLeave"
                    @drop="onFileDrop"
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
        <ul v-if="files.length" class="files-list">
            <li v-for="(file, index) in files" :key="index">
                <div class="file-name" :title="file.name">{{ file.name }}</div>
                <button @click="removeFile(index)" class="remove-file-button">
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
    margin-bottom: 25px;
    width: 75%;
}

.upload-question-container > * {
    margin-inline: 50%;
    transform: translateX(-50%);
    width: 100%;
}

.allowed-info {
    display: flex;
    justify-content: flex-start;
    font-size: 0.9em;
}

.allowed-info div {
    width: 100%;
}

.drag-drop-outer {
    height: 150px;
    padding: 6px;
    border-radius: 12px;
    border: 2px solid var(--palette-mobster);
}

.dragover {
    background-color: var(--palette-foam);
}

.dragleave {
    background-color: white;
}

.drag-drop-inner {
    display: flex;
    align-items: center;
    justify-content: center;
    box-sizing: border-box;
    font-size: 0.9em;
    height: 100%;
    border-radius: 6px;
    border: 2px dashed var(--palette-mobster);
}

.drag-drop-inner input {
    display: none;
}

.drag-drop-inner label {
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    flex-direction: column;
    width: 100%;
    height: 100%;
}

.files-list {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 0;
    margin-bottom: 0;
}

.files-list li {
    display: flex;
    align-items: center;
    justify-content: space-between;
    width: 60%;
    max-width: 60%;
    padding-block: 5px;
    border-top: thin solid black;
}

@media only screen and (max-width: 600px) {
    .upload-question-container {
        width: 100%;
    }

    .allowed-info {
        flex-direction: column;
        text-align: left;
        padding-left: 60px;
    }

    .drag-drop-outer {
        width: 90%;
    }

    .files-list {
        width: 100%;
        padding: 0;
    }

    .files-list li {
        width: 100%;
        max-width: 100%;
    }
}

.files-list li:first-child {
    border: none;
}

.files-list li .file-name {
    flex: 1;
    text-align: left;
    font-style: italic;
    font-size: 0.9em;
    text-overflow: ellipsis;
    white-space: nowrap;
    overflow: hidden;
}

.files-list li .remove-file-button {
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
