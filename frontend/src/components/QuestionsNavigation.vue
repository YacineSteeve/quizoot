<script setup lang="ts">
import NavigationButton from '@/components/NavigationButton.vue';

interface QuestionsNavigationProps {
    showNext: boolean;
    showPrevious: boolean;
    goToPreviousQuestion: () => void;
    goToNextQuestion: () => void;
    onSubmit?: () => void;
}

const props = defineProps<QuestionsNavigationProps>();

function goTo(s: 'next' | 'previous') {
    switch (s) {
        case 'next':
            props.goToNextQuestion();
            break;
        case 'previous':
            props.goToPreviousQuestion();
            break;
        default:
            break;
    }
}
</script>

<template>
    <div class="navigation-button-group">
        <navigation-button
            v-if="props.showPrevious"
            @click="goTo('previous')"
            backgroundColor="var(--palette-mobster)"
            chevronLeft
            class="previous-button button"
        >
            Previous
        </navigation-button>
        <div class="button-separator"></div>
        <navigation-button
            v-if="props.showNext"
            @click="goTo('next')"
            backgroundColor="var(--main-purple-lightened)"
            chevronRight
            class="next-button button"
        >
            Next
        </navigation-button>
        <div
            v-if="props.showPrevious && !props.showNext"
            class="button-separator"
        ></div>
        <navigation-button
            v-if="props.onSubmit && props.showPrevious && !props.showNext"
            @click="props.onSubmit"
            backgroundColor="var(--palette-cutty-sark)"
            class="submit-button button"
        >
            Submit
        </navigation-button>
    </div>
</template>

<style scoped>
.navigation-button-group {
    display: flex;
    align-items: center;
    justify-content: space-between;
    width: 80%;
    margin-top: 1em;
}

.button-separator {
    width: 1px;
    height: 100%;
}

.navigation-button-group .button {
    min-width: 150px;
}

@media only screen and (max-width: 600px) {
    .navigation-button-group {
        width: 100%;
    }
}
</style>
