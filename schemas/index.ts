import * as tjs from 'typescript-json-schema';
import path from 'path';
import * as fs from 'fs';

// Arguments to be passed to schema generator
const settings: tjs.PartialArgs = {
    required: true,
};

const schemasToGenerate = [
    {
        type: 'Quizoot.Question',
        name: 'question'
    },
    {
        type: 'Quizoot.Quiz',
        name: 'quiz'
    }
];

const sourceFilePath = path.join(__dirname, './interface.ts');

schemasToGenerate.forEach((schema) => {
    const program = tjs.getProgramFromFiles([path.resolve(sourceFilePath)]);
    const definition = tjs.generateSchema(program, schema.type, settings);
    
    try {
        fs.writeFileSync(`./${schema.name}.json`, JSON.stringify(definition));
    } catch (err) {
        console.error(err);
    }

});