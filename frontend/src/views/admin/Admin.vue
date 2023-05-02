<script setup lang="ts">
</script>

<template>
    <div class="admin-container">
        <h1>Admin</h1>
        <RouterView />
    </div>
</template>

<style scoped>
.admin-container {
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    width: 140%;
    min-height: 100vh;
    padding-bottom: 30px;
}

h1 {
    font-size: 3em;
    font-weight: 600;
    padding: 0;
}
</style>
