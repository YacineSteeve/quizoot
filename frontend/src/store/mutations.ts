import type { MutationTree } from 'vuex';
import type { State } from '@/store/state';
import { MutationTypes } from '@/store/types';

export type Mutations<S = State> = {
    [MutationTypes.UPDATE_QUIZZES](
        state: S,
        quizzesList: State['quizzes']
    ): void;
    [MutationTypes.UPDATE_CURRENT_QUIZ](
        state: S,
        quiz: State['currentQuiz']
    ): void;
};

export const mutations: MutationTree<State> & Mutations = {
    [MutationTypes.UPDATE_QUIZZES](state, quizzesList: State['quizzes']) {
        state.quizzes = quizzesList;
    },
    [MutationTypes.UPDATE_CURRENT_QUIZ](state, quiz: State['currentQuiz']) {
        state.currentQuiz = quiz;
    },
};
