<script setup lang="ts"></script>

<template>
    <div>
        <div class="navbar">
            <ul class="links">
                <li class="menu-item">
                    <router-link to="/" title="Home"> Home </router-link>
                </li>
                <li class="menu-item">
                    <router-link to="/news" title="News"> News </router-link>
                </li>
                <li id="logo">
                    <router-link to="/" title="Logo">
                        <img
                            src="../assets/logo-no-background.svg"
                            alt="Quizoot Logo"
                        />
                    </router-link>
                </li>
                <li class="menu-item">
                    <router-link to="/contact" title="Contact">
                        Contact
                    </router-link>
                </li>
                <li class="menu-item">
                    <router-link to="/about" title="About"> About </router-link>
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
    background-color: var(--main-purple);
    width: 100%;
    height: 3.5em;
    z-index: 99;
}

.links {
    display: flex;
    align-items: center;
    flex-shrink: 0;
    width: 45vw;
    min-width: 500px;
    height: 100%;
    margin: 0;
    padding: 0;
    list-style-type: none;
}

.links li#logo {
    width: fit-content;
    height: fit-content;
    margin-inline: 4vw;
}

.links li#logo img {
    width: auto;
    height: 2.5em;
}

.links li.menu-item {
    flex: 1;
    height: 60%;
}

.links li.menu-item a {
    color: var(--text-yellow-lightened);
    display: flex;
    align-items: center;
    justify-content: center;
    text-decoration: none;
    font-weight: 600;
    font-size: 1em;
    width: 100%;
    height: 100%;
}

@media only screen and (max-width: 600px) {
    .links {
        width: 100%;
        min-width: min-content;
    }

    .links li#logo {
        width: 25%;
        margin-inline: 3%;
    }

    .links li#logo img {
        width: 100%;
        height: auto;
    }

    .links li.menu-item a {
        font-size: 0.8em;
    }
}

.links li.menu-item:hover {
    background-color: var(--menu-hover-pink);
    border-radius: 5px;
}
</style>
