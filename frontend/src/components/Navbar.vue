<script setup lang="ts">
</script>

<template>
    <div>
        <div class="navbar">
            <ul class="links">
                <li>
                    <a href="#home" class="menu-item">Home</a>
                </li>
                <li>
                    <a href="#news" class="menu-item">News</a>
                </li>
                <li id="logo">
                    <a href="#">
                        <img src="../assets/logo-no-background.svg"/>
                    </a>
                </li>
                <li>
                    <a href="#contact" class="menu-item">Contact</a>
                </li>
                <li>
                    <a href="#about" class="menu-item">About</a>
                </li>
            </ul>
        </div>
    </div>
</template>

<style scoped>

.navbar {
    position: fixed;
    top: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 0;
    padding: 0;
    overflow: hidden;
    background-color: var(--main-blue);
    width: 100%;
    height: 10vh;
}

.navbar img {
    width: 150px;
    height: auto;
}

.links {
    list-style-type: none;
    display: flex;
    width: 40%;
    align-items: center;
    justify-content: space-between;
}

.links li#logo {
    margin-inline: 5%;
}

.links li a {
    color: var(--text-yellow);
    text-align: center;
    font-weight: 600;
    font-size: large;
    padding: 14px 16px;
    text-decoration: none;
}

.links li a.menu-item:hover:not(.active) {
    background-color: var(--menu-hover-pink);
    border-radius: 5px;
}
</style>
