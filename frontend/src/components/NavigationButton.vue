<script setup lang="ts">
interface NavigateButtonProps {
    backgroundColor: string;
    chevronLeft?: boolean;
    chevronRight?: boolean;
}

const props = defineProps<NavigateButtonProps>();
</script>

<template>
    <div class="navigation-button-container">
        <button>
            <span v-if="props.chevronLeft">&#171;</span>
            <slot></slot>
            <span v-if="props.chevronRight">&#187;</span>
        </button>
    </div>
</template>

<style scoped>
.navigation-button-container button {
    background-color: v-bind('props.backgroundColor');
    color: white;
    font-weight: 600;
    font-size: 1.1em;
    padding-left: 10px;
    padding-right: 10px;
    width: 100%;
    min-height: 50px;
    border-radius: 10px;
    cursor: pointer;
    border: none;
    box-shadow: 0 0 3px 1px dimgray;
}

.navigation-button-container button:hover {
    transform: scale(0.98);
    opacity: 0.8;
}
</style>
