<script setup lang="ts">
import type { Quizoot } from '@interfaces/quizoot';
import Manage from '@/components/Manage.vue';

</script>

<template>
    <Manage elements="Quizzes">
        <template #authors="{value: authors}">
            <ul>
                <li v-for="author in authors as Quizoot.Author[]">
                    {{ author.name }} &nbsp;
                    {{ author.surname ?? '' }} &nbsp;
                    {{ author.pseudo ? `(${author.pseudo})` : '' }} &nbsp;
                    {{ author.email ? `<${author.email}>` : '' }}
                </li>
            </ul>
        </template>
    </Manage>
</template>

<style scoped>

</style>
