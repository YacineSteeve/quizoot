import type { Quizoot } from 'quizoot';

export interface Quiz extends Quizoot.Quiz {
    [x: string]: any;
}
