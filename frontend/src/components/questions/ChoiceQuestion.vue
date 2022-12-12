<script setup lang="ts">
import { ref, computed } from 'vue';
import type { Ref } from 'vue';
import type { Quizoot } from '@interfaces/quizoot';

interface ChoiceQuestionProps {
    spec: Quizoot.ChoiceQuestion;
}

const props = defineProps<ChoiceQuestionProps>();

const isSingleChoiceQuestion = (
    spec: Quizoot.ChoiceQuestion
): spec is Quizoot.SingleChoiceQuestion => {
    return 'answer_id' in spec;
};

type InputType = 'checkbox' | 'radio';

const answers: Ref<Set<Quizoot.OptionId>> = ref(new Set());

const inputType = computed<InputType>(() =>
    isSingleChoiceQuestion(props.spec) ? 'radio' : 'checkbox'
);

function onSelect(event: Event) {
    const target = event.target as HTMLInputElement;
    if (target.checked) {
        answers.value.add(target.id);
    } else {
        answers.value.delete(target.id);
    }
}
</script>

<template>
    <div class="choices">
        <ul>
            <li v-for="option in spec.options" :key="option.id">
                <input
                    :type="inputType"
                    :id="option.id"
                    name="choice"
                    @change="onSelect"
                />
                <label>{{ option.display }}</label>
            </li>
        </ul>
    </div>
</template>

<style scoped>
.choices {
    width: 80%;
    text-align: left;
    font-size: 1.2em;
    margin: 0;
}

.choices ul {
    list-style: none;
}

.choices li {
    margin-block: 20px;
}

.choices input {
    margin-inline-end: 10px;
}
</style>
