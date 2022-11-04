<script setup lang="ts">
import QuizCard from "@/components/QuizCard.vue";

</script>

<template>
    <div class="main-container">
        <div class="main">
            <QuizCard v-for="num in [1, 2, 3, 4, 5, 6, 7]" v-bind:index="num"/>
        </div>
    </div>
</template>

<style scoped>

.main-container {
    width: 100%;
    height: 90vh;
    margin-top: 10vh;
    background-color: var(--background-color);
    overflow: scroll;
}

.main-container::-webkit-scrollbar {
    width: 10px;
    height: 100%;
    background: var(--light-grey);
}

.main-container::-webkit-scrollbar-thumb {
    background: var(--main-blue-lightened);
    border-radius: 4px;
}

.main-container::-webkit-scrollbar-thumb:hover {
    background: var(--main-blue);
}

.main {
    height: 100%;
    margin-inline: 20vw;
}

</style>
