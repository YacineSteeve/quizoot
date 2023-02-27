<script setup lang="ts">
interface ProgressBarProps {
    currentStep: number;
    totalSteps: number;
}

const props = defineProps<ProgressBarProps>();
</script>

<template>
    <div class="progressbar-container">
        <div
            v-for="index in props.totalSteps"
            class="step"
            :class="{ passed: props.currentStep >= index }"
        >
            <div v-if="index > 1" class="separator"></div>
            <div class="indicator">
                {{ index }}
            </div>
        </div>
    </div>
</template>

<style scoped>
.progressbar-container {
    --progress-bar-width: 50vw;
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: center;
    width: var(--progress-bar-width);
    margin-block: 1em;
}

.step {
    display: flex;
    align-items: center;
    justify-content: center;
}

.indicator {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 1.75em;
    height: 1.75em;
    border-radius: 50%;
    background-color: var(--palette-spun-pearl);
}

.separator {
    flex: 1;
    width: calc(
        (var(--progress-bar-width) - v-bind('props.totalSteps') * 1.75em) / 4
    );
    height: 2px;
    background-color: var(--palette-spun-pearl);
}

.step.passed .indicator,
.step.passed .separator {
    background-color: var(--palette-carribean-green);
}

@media only screen and (max-width: 600px) {
    .progressbar-container {
        --progress-bar-width: 85vw;
    }
}
</style>
