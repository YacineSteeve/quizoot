import { Quizoot } from 'quizoot';

export interface Quiz extends Quizoot.Quiz {
    [x: string]: any;
}

export interface Question extends Quizoot.Question {
    [x: string]: any;
}
