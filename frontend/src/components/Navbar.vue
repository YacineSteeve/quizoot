<script setup lang="ts"></script>

<template>
    <div>
        <div class="navbar">
            <ul class="links">
                <li>
                    <router-link to="/" title="Home" class="menu-item">
                        Home
                    </router-link>
                </li>
                <li>
                    <router-link to="/news" title="News" class="menu-item">
                        News
                    </router-link>
                </li>
                <li id="logo">
                    <router-link to="/" title="Logo">
                        <img
                            src="../assets/logo-no-background.svg"
                            alt="Quizoot Logo"
                        />
                    </router-link>
                </li>
                <li>
                    <router-link
                        to="/contact"
                        title="Contact"
                        class="menu-item"
                    >
                        Contact
                    </router-link>
                </li>
                <li>
                    <router-link to="/about" title="About" class="menu-item">
                        About
                    </router-link>
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
    width: 45%;
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
    font-size: medium;
    padding: 14px 16px;
    text-decoration: none;
}

.links li a.menu-item:hover:not(.active) {
    background-color: var(--menu-hover-pink);
    border-radius: 5px;
}
</style>
