export declare namespace Quizoot {
    /**
     * Question object used to create a quiz. A Quiz is a set of questions.
     *
     * @version 0.1.0
     */
    export interface Question {
        /**
         * Id of the question
         * 
         * @pattern [a-z0-9]{24}
         */
        id: string;
        /**
         * The actual question as a human-readable string.
         */
        question: string;
        /** 
         * The question kind. Please refer to {@link QuestionKind}.
         */
        kind: QuestionKind;
        /** 
         * Spec of the question. It specifies what the attributes of the question are. Attributes depends on {@link QuestionKind}.
         * 
         * See {@link QuestionSpec} for more information about the spec attributes for each question kind.
         */
        spec: QuestionSpec;
        /** 
         * The grading object specifies how to grade for the current question. See {@link Grading}.
        */
        grading: Grading;
        /** 
         * Rate how difficult the question is. See {@link Difficulty}.
         */
        difficulty: Difficulty;
        /** 
         * List of optional tags associated with the question.
         */
        tags?: string[];
        /** 
         * Hint given to help answering the question 
         */
        hint?: string;
    }

    /** 
     * Different kind of question we might have.
     */
    type QuestionKind = "CHOICE_QUESTION" | "TEXT_QUESTION" | "UPLOAD_QUESTION" | "CODE_QUESTION";

    interface Grading {
        /**
         * Specifies how much a correct answer count for in the total score.
         */
        point_value: number;
        /**
         * Feedback given after answering the question.
         */
        feedback: Feedback;
    }

    interface Feedback {
        /** 
         * General feedback/explanation displayed whether the answer is wrong or correct. 
         */
        explanation: string;
        /**
         * Feedback when answer is wrong.
         */
        when_wrong?: string;
        /**
         * Feedback when answer is right.
         */
        when_right?: string;
    }

    /** 
     * Question difficulty: easy, medium or hard.
     */
    type Difficulty = "EASY" | "MEDIUM" | "HARD";

    /**
     * Question spec. It depends on the question kind.
     */
    type QuestionSpec = ChoiceQuestion | TextQuestion | UploadQuestion | CodeQuestion;

    /**
     * Choice question : can either be a [Single Choice Question]{@link SingleChoiceQuestion} or a [Multiple Choices Question]{@link MultipleChoicesQuestion}.
     */
    type ChoiceQuestion = SingleChoiceQuestion | MultipleChoicesQuestion;

    interface SingleChoiceQuestion {
        /**
         * Question options. See {@link QuestionOption}.
         */
        options: QuestionOption[]
        /**
         * Id of the correct answer to the question.
         */
        answer_id: OptionId;
    }

    interface MultipleChoicesQuestion {
        /**
         * Question options. See {@link QuestionOption}.
         */
        options: QuestionOption[]
        /**
         * Id of the correct answers to the question.
         */
        answers_id: OptionId[];
    }

    interface QuestionOption {
        /**
         * Id of the option.
         */
        id: OptionId;
        /**
         * The actual display of the option as a human-readable string.
         */
        display: string;
    }

    type OptionId = string;

    interface TextQuestion {
        /**
         * Placeholder to display in the html `textarea` or `input`
         * 
         * @examples ["Type your text here..."]
         */
        placeholder?: string;
        /**
         * List of keywords that the answers should contain. It is up to the developer to implement if the answer should contain ALL or ANY of the keywords.
         * 
         * @examples ["bytes", "octets"]
         */
        keywords?: string[];
    }

    interface UploadQuestion {
        /**
         * List of files to upload.
         */
        files: File[];
        /**
         * Maximum size of each files. Can be expressed in bytes, megabytes (MB), etc. See TODO for valid units.
         * 
         * @examples ["10MB"]
         */
        max_size: string;
        /** 
         * Maximum number of files to upload.
         * 
         * @default 1
         * @minimum 1
         */
        max_files: number;
    }

    interface File {
        /**
         * File type enum. Can be `.txt`, `.csv`, `.pdf`, etc. See {@link FileType}.
         */
        type: FileType;
        /**
         * Encoded `base64` string of the file's content.
         */
        content: string;
    }

    /**
     * Enum of supported file extensions.
     */
    type FileType = ".txt" | ".csv" | ".pdf" | ".img" | ".jpg" | ".jpeg" | ".png";

    interface CodeQuestion  {
        /**
         * Code content. This will be run using a `python3` runner and evaluated.
         */
        content: string;
        /**
         * Coding language. Only `python3` is supported.
         */
        language: "python3";
        /**
         * Expected output after running the code.
         */
        expected_output: string;
    }

    /**
     * A Quiz object represents a set of questions.
     *
     * @version 0.1.0
     */
    export interface Quiz {
        /**
         * Id of the quiz.
         *
         * @pattern [a-z0-9]{24}
         */
        id: string;
        /**
         * The title (header) of the quiz.
         *
         * @minLength 1
         * @maxLength 40
         */
        title: string;
        /**
         * A brief description of the quiz content, topic...
         */
        description: string;
        /**
         * Maximum score the user can get. Will be used to compute the final score: sum(question_i_score) / max_score.
         *
         * @default 0
         * @minimum 0
         */
        max_score: number;
        /**
         * All the questions the quiz is made of.
         */
        questions: Question[]
        /**
         * List of optional authors or contributors of the quiz. See {@link Author}.
         */
        authors?: Author[];
        /**
         * List of optional tags associated with the quiz.
         */
        tags?: string[];
    }

    interface QuestionItem {
        /**
         * Id of a question referenced in the quiz.
         *
         * @pattern [a-z0-9]{24}
         */
        question_id: string;
        /**
         * Id of the next question in the quiz chronology. Is null if it is the last question.
         */
        next_question_id: string | null;
        /**
         * Id of the previous question in the quiz chronology. Is null if it is the first question.
         */
        prev_question_id: string | null;
    }

    interface Author {
        /**
         * The quiz author's first name.
         */
        name: string;
        /**
         * The quiz author's last name. Is optional.
         */
        surname?: string;
        /**
         * A pseudo for the quiz author.
         */
        pseudo?: string | null;
        /**
         * The quiz author's email.
         *
         * @pattern ^[a-zA-Z]+[\w.\d-]*@[a-zA-Z]+\.[a-zA-Z]{1,3}$
         */
        email?: string;
    }
}
