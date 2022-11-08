<script setup lang="ts"></script>

<template>
    <div class="main-container">
        <div class="main">
            <router-view></router-view>
        </div>
    </div>
</template>

<style scoped>
.main-container {
    width: 100%;
    height: auto;
    margin-top: 10vh;
    background-color: var(--background-color);
}

.main {
    margin-inline: 20vw;
}
</style>
