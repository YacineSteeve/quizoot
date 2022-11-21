
/**
 * Question objects used to create a quiz. A Quiz is a set of questions
 * 
 * @version 0.1.0
 */
export interface Question {
    /**
     * Id of the question
     * 
     * @pattern [a-z0-9]{12}
     */
    id: string;
    /**
     * The actual question as a human readable string.
     */
    question: string;
}
