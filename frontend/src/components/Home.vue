<script setup lang="ts">
    import QuizCard from'@/components/QuizCard.vue';

    // Retrieve quizzes list (maybe from routed url params) and pass it to the template
</script>

<template>
    <div class="home-container">
        <div class="">
            <h1>Get Started</h1>
        </div>
        <!-- Quiz details will be inserted as attributes to QuizCard components
            for each quiz in quizzes list -->
        <QuizCard v-for="num in [1, 2, 3, 4, 5, 6, 7]" v-bind:index="num"/>
    </div>
</template>

<style scoped>
.home-container {
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: center;
    width: 100%;
    height: 100%;
}
</style>
