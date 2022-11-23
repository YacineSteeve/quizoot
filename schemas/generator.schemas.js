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
        typeName: 'Quizoot.Question',
        schemaName: 'question'
    },
    {
        typeName: 'Quizoot.Quiz',
        schemaName: 'quiz'
    }
];

const sourceFilePath = './interface.ts';

schemasToGenerate.forEach((obj) => {
    const program = TJS.getProgramFromFiles([resolve(sourceFilePath)]);

    const schema = TJS.generateSchema(program, obj.typeName, settings);

    // TODO: Write the schema in a .json file
    try {
        fs.writeFileSync(`./${obj.schemaName}.json`, JSON.stringify(schema.contains));
    } catch (err) {
        console.error(err);
    }

})
