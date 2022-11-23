<script setup lang="ts">
</script> 

<template>
    <div class="quiz-container">
        <h1 class="quiz-title">Basic Data Types in Python Quiz</h1>
        <div class="quiz-subtitle">
            Interactive Quiz <span>&#8226;</span> <span class="question-count">20</span> Questions
            <p>By Author Name</p>
        </div>
        <div class="quiz-content">
            <p>
                Test your understanding of the basic data types that are built into Python, like numbers, strings,
                and
                Booleans.
            </p>
        </div>
        <div class="btn-group">
            <button>
                Start the quiz <span>&#187;</span>
            </button>
        </div>
    </div>

</template>

<style>
.quiz-container {
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: center;
    width: 65%;
    margin-left: 17.5%;
    margin-right: 17.5%;
    padding-bottom: 30px;
    min-height: 60vh;
}

.quiz-title {
    margin-bottom: 0;
}

.quiz-subtitle {
    margin-top: 5px;
}

.quiz-content {
    text-align: left;
    font-size: 1.2em;
}

.question-count {
    font-weight: 800;
    color: var(--text-yellow);
}

.btn-group {
    display: flex;
    width: 100%;
    justify-content: flex-end;
    align-items: center;
}

.btn-group button {
    background-color: #34a853;
    color: white;
    font-weight: 600;
    font-size: 1.1em;
    padding-left: 10px;
    padding-right: 10px;
    width: auto;
    min-height: 40px;
    border-radius: 5px;
    cursor: pointer;
    border: none;
}

.btn-group button:hover {
    transform: translate(2px, 2px);
    opacity: 0.8;
}
</style>