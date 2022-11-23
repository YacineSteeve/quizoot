import { Quizoot } from "./question";

export interface Quiz {
    /**
     * Nothing
     */
    id: string;
    /**
     * Nothing
     */
    title: string;
    /**
     * Nothing
     */
    description: string;
    /**
     * Nothing
     */
    questions: Quizoot.Question[];
}
