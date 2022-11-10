<script setup lang="ts">
import Navbar from '@/components/Navbar.vue';
import Footer from '@/components/Footer.vue';

</script>

<template>
    <Navbar />
    <div class="main-container">
        <div class="main">
            <router-view></router-view>
        </div>
    </div>
    <Footer />
</template>

<style>
@import './styles/main.css';

#app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    display: flex;
    flex-direction: column;
}

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
