import { describe, it } from 'mocha';
import { pascalToSnake, snakeToPascal, capitalize } from '../string-utils';
import assert from 'assert';

describe('string-utils', () => {
    describe('.pascalToSnake', () => {
        it('converted ChoiceQuestion', () => {
            const input = 'ChoiceQuestion';
            const expectedOutput = 'choice_question';
            assert.strictEqual(pascalToSnake(input), expectedOutput);
        });

        it('converted MotorRPM', () => {
            const input = 'MotorRPM';
            const expectedOutput = 'motor_rpm';
            assert.strictEqual(pascalToSnake(input), expectedOutput);
        });

        it('noop for snake_case', () => {
            const input = 'snake_case';
            const expectedOutput = 'snake_case';
            assert.strictEqual(pascalToSnake(input), expectedOutput);
        });

        it('bonus: converted camelCase', () => {
            const input = 'camelCase';
            const expectedOutput = 'camel_case';
            assert.strictEqual(pascalToSnake(input), expectedOutput);
        });
    });

    describe('.snakeToPascal', () => {
        it('converted choice_question', () => {
            const input = 'choice_question';
            const expectedOutput = 'ChoiceQuestion';
            assert.strictEqual(snakeToPascal(input), expectedOutput);
        });

        it('converted motor_rpm', () => {
            const input = 'motor_rpm';
            const expectedOutput = 'MotorRpm';
            assert.strictEqual(snakeToPascal(input), expectedOutput);
        });

        it('noop for PascalCase', () => {
            const input = 'PascalCase';
            const expectedOutput = 'PascalCase';
            assert.strictEqual(snakeToPascal(input), expectedOutput);
        });

        it('bonus: converted camel_case', () => {
            const input = 'camel_case';
            const expectedOutput = 'CamelCase';
            assert.strictEqual(snakeToPascal(input), expectedOutput);
        });
    });

    describe('.capitalize', () => {
        it('capitalized first letter', () => {
            const input = 'hello world';
            const expectedOutput = 'Hello world';
            assert.strictEqual(capitalize(input), expectedOutput);
        });

        it('noop for capitalized first letter', () => {
            const input = 'Hello world';
            const expectedOutput = 'Hello world';
            assert.strictEqual(capitalize(input), expectedOutput);
        });
    });
});
