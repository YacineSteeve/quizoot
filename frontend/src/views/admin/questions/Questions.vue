<script setup lang="ts">
import type { Quizoot } from '@interfaces/quizoot';
import Manage from '@/components/Manage.vue';
</script>

<template>
    <Manage elements="Questions">
        <template #spec="{ value: questionSpec }">
            <ul class="spec">
                <li v-for="(spec, key) in questionSpec" :key="key">
                    <span class="key">{{ key }}: </span>
                    <ul v-if="Array.isArray(spec)">
                        <li v-for="(value, index) in spec" :key="index">
                            <span>{{ value }}</span>
                        </li>
                    </ul>
                    <span v-else>{{ spec }}</span>
                </li>
            </ul>
        </template>
        <template #grading="{ value: grading }">
            <ul class="grading">
                <li>
                    <span>Point Value:</span>
                    {{ (grading as Quizoot.Grading).point_value }}
                </li>
                <li>
                    <span>Feedback:</span>
                    {{ (grading as Quizoot.Grading).feedback.explanation }}
                </li>
            </ul>
        </template>
    </Manage>
</template>

<style scoped>
.spec,
.grading {
    list-style-type: square;
    text-align: left;
}

.spec li,
.grading li {
    margin: 0.5rem 0;
}

.spec li span.key,
.grading li span {
    font-weight: bold;
}
</style>
