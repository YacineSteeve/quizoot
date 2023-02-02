import type { Quiz } from '@interfaces/quizoot.indexed';

export const state = {
    quizzes: null,
}

export type State = {
    quizzes: Quiz[] | null
}
