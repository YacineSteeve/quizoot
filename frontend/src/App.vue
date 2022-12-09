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
        <Footer />
    </div>
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
    height: calc(100vh - 3.5em);
    margin-top: 3.5em;
    background-color: var(--background-color);
    overflow: scroll;
}

.main-container::-webkit-scrollbar {
    width: 5px;
    height: 100%;
    background: var(--light-grey);
}

.main-container::-webkit-scrollbar-thumb {
    background: var(--main-purple-lightened);
    border-radius: 4px;
}

.main-container::-webkit-scrollbar-thumb:hover {
    background: var(--main-purple);
}

.main {
    min-height: calc(100vh - 3.5em);
    padding-top: 1em;
    padding-bottom: 3.5em;
}

@media only screen and (min-width: 600px) {
    .main {
        margin-left: 20vw;
        margin-right: calc(20vw - 10px);
    }

    .main-container::-webkit-scrollbar {
        width: 10px;
    }
}
</style>
