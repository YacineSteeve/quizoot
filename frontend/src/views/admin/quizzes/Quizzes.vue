<script setup lang="ts">
import type { Quizoot } from '@interfaces/quizoot';
import AdminManage from '@/components/AdminManage.vue';
</script>

<template>
    <admin-manage elements="Quizzes">
        <template #authors="{ value: authors }">
            <ul>
                <li v-for="author in authors as Quizoot.Author[]" :key="author">
                    {{ author.name }} &nbsp; {{ author.surname ?? '' }} &nbsp;
                    {{ author.pseudo ? `(${author.pseudo})` : '' }} &nbsp;
                    {{ author.email ? `<${author.email}>` : '' }}
                </li>
            </ul>
        </template>
    </admin-manage>
</template>

<style scoped></style>
