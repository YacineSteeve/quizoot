import * as fs from 'fs';
import * as tjs from 'typescript-json-schema';

import path from 'path';

const SCHEMAS_DIR = path.join(__dirname, "./schemas");
const SOURCE_FILE_PATH = path.join(__dirname, './quizoot.ts');

// Arguments to be passed to schema generator
const SETTINGS: tjs.PartialArgs = {
    required: true,
};

const SCHEMAS_TO_GENERATE = [
    {
        type: 'Quizoot.Question',
        name: 'question'
    },
    {
        type: 'Quizoot.Quiz',
        name: 'quiz'
    }
];


SCHEMAS_TO_GENERATE.forEach((schema) => {
    const program = tjs.getProgramFromFiles([path.resolve(SOURCE_FILE_PATH)]);
    const definition = tjs.generateSchema(program, schema.type, SETTINGS);
    
    try {
        const filepath = path.join(SCHEMAS_DIR, `./${schema.name}.json`)
        fs.writeFileSync(filepath, JSON.stringify(definition, null, 2) + '\n');
    } catch (err) {
        console.error(err);
    }
});
