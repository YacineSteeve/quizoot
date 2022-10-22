<script setup lang="ts">
import HelloWorld from './components/HelloWorld.vue';
import Navbar from './components/Navbar.vue';
</script>

<template>
    <Navbar />
    <div class="container">
        <HelloWorld name=" World!" />
    </div>
</template>

<style>
@import "./styles/main.css";

#app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    margin-top: 60px;
}
</style>
