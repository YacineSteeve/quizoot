import type { Quiz } from '@interfaces/quizoot.indexed';

export const state = {
    quizzes: null,
    currentQuiz: null,
};

export type State = {
    quizzes: Quiz[] | null;
    currentQuiz: Quiz | null;
};
