import { describe, it } from 'mocha';
import { pascalToSnake } from '../string-utils';
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
});
