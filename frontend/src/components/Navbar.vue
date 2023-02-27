<script setup lang="ts">
import { ref, watch } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const current = ref(0);
const nonMenuViews = ['Quiz'];

watch(
    () => route.matched[0]?.name,
    (name: string) => {
        if (nonMenuViews.includes(name)) {
            current.value = 0;
        }
    }
);

function setActive(index: number) {
    current.value = index;
}
</script>

<template>
    <div>
        <div class="navbar">
            <ul class="links">
                <li
                    class="menu-item"
                    :class="{ isCurrent: current === 1 }"
                    @click="setActive(1)"
                >
                    <router-link to="/" title="Home"> Home </router-link>
                </li>
                <li
                    class="menu-item"
                    :class="{ isCurrent: current === 2 }"
                    @click="setActive(2)"
                >
                    <router-link to="/contact" title="Contact">
                        Contact
                    </router-link>
                </li>
                <li id="logo" @click="setActive(0)">
                    <router-link to="/" title="Logo">
                        <img
                            src="../assets/logo-no-background.svg"
                            alt="Quizoot Logo"
                        />
                    </router-link>
                </li>
                <li
                    class="menu-item"
                    :class="{ isCurrent: current === 3 }"
                    @click="setActive(3)"
                >
                    <router-link to="/signup" title="Sign Up">
                        Sign Up
                    </router-link>
                </li>
                <li
                    class="menu-item"
                    :class="{ isCurrent: current === 4 }"
                    @click="setActive(4)"
                >
                    <router-link to="/login" title="Login"> Login </router-link>
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
    gap: 2px;
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
    border-radius: 5px;
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

.links li.menu-item.isCurrent,
.links li.menu-item:hover {
    background-color: var(--menu-hover-pink);
}
</style>
