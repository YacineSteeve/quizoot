<script setup lang="ts">
</script>

<template>
    <div class="admin-landing-container">
        <h2>Choose a section to manage</h2>
        <div class="choices">
            <router-link to="/admin/quizzes">Quizzes</router-link>
            <router-link to="/admin/questions">Questions</router-link>
        </div>
    </div>
</template>

<style scoped>
.choices {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
    height: 100%;
}

a {
    display: block;
    margin: 0.5em;
    padding: 0.5em;
    border: 1px solid var(--main-purple);
    border-radius: 5px;
    text-decoration: none;
    color: var(--main-purple);
    font-size: 1.5em;
    font-weight: 600;
    text-align: center;
    width: 10em;
}

a:hover {
    background-color: var(--main-purple);
    color: var(--text-yellow-lightened);
}
</style>
