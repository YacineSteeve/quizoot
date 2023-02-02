import type { MutationTree } from 'vuex';
import type { State } from '@/store/state';
import { MutationTypes } from '@/store/types';

export type Mutations<S = State> = {
    [MutationTypes.UPDATE_QUIZZES](state: S, quizzesList: State['quizzes']): void;
}

export const mutations: MutationTree<State> & Mutations = {
    [MutationTypes.UPDATE_QUIZZES](state, quizzesList: State['quizzes']) {
        state.quizzes = quizzesList
    }
}
