import { resolve } from 'path';
import * as TJS from 'typescript-json-schema';
import * as fs from 'fs';

// Arguments to be passed to schema generator
const settings = {
    noExtraProps: true,
    aliasRefs: true
};

const schemasToGenerate = [
    {
        filePath: './question.ts',
        typeName: 'Quizoot.Question',
        schemaName: 'question'
    },
    {
        filePath: './quiz.ts',
        typeName: 'Quizoot.Quiz',
        schemaName: 'quiz'
    }
];

schemasToGenerate.forEach((obj) => {
    const program = TJS.getProgramFromFiles([resolve(obj.filePath)]);

    const schema = TJS.generateSchema(program, obj.typeName, settings);

    // TODO: Write the schema in a .json file
    try {
        fs.writeFileSync(`./${obj.schemaName}.json`, JSON.stringify(schema.contains));
    } catch (err) {
        console.error(err);
    }

})
