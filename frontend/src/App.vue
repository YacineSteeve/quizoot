<script setup lang="ts">
import Navbar from '@/components/Navbar.vue';
import Main from "@/components/Main.vue";
</script>

<template>
    <Navbar />
    <Main />
</template>

<style>
@import "./styles/main.css";

#app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    display: flex;
    flex-direction: column;
}
</style>
