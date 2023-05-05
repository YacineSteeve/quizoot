import * as fs from 'fs';
import * as tjs from 'typescript-json-schema';

import path from 'path';

const SCHEMAS_DIR = path.join(__dirname, './schemas');
const SOURCE_FILE_PATH = path.join(__dirname, './quizoot.ts');

// Arguments to be passed to schema generator
const SETTINGS: tjs.PartialArgs = {
	required: true,
};

const program = tjs.getProgramFromFiles([path.resolve(SOURCE_FILE_PATH)]);

async function main() {
	const schema = generateSchema('QuestionKind');
	await saveSchema('question_kind', schema);

	const questionKinds = ((schema?.enum as string[]) ?? []).map((s) =>
		s.toLowerCase()
	);

	// Generate appropriate schema for each kind of question
	for (const kind of questionKinds) {
		try {
			const schema = generateSchema(snakeToPascal(kind));
			await saveSchema(kind, schema);
		} catch (err) {
			console.error('Could not generate schema', kind);
		}
	}

	// Generate question schema (union of all questions)
	await saveSchema('question', generateSchema('Question'));

	// Generate quiz schema
	await saveSchema('quiz', generateSchema('Quiz'));

	// Generate index.ts file
	await generateIndexFile(['quiz', 'question', 'question_kind', ...questionKinds]);
}

function generateSchema(typeName: string) {
	console.log(`[INFO] Generating "Quizoot.${typeName}" schema`);
	return tjs.generateSchema(program, `Quizoot.${typeName}`, SETTINGS);
}

async function saveSchema(name: string, schema: tjs.Definition | null) {
	return fs.writeFile(
		path.join(SCHEMAS_DIR, `${name}.json`),
		JSON.stringify(schema, null, 4),
		(err) => {
			if (err) {
				console.error(`unable to save ${name} schema.`);
			}
		}
	);
}

async function generateIndexFile(schemasNames: string[]) {
	const indexFileContent = schemasNames
		.map((name) => `export { default as ${snakeToPascal(name)}Schema } from './${name}.json';`)
		.join('\n\n');

	console.log('[INFO] Generating index file')
	return fs.writeFile(
		path.join(SCHEMAS_DIR, 'index.ts'),
		indexFileContent,
		(err) => {
			if (err) {
				console.error(`Unable to generate index file.`);
			}
		}
	);
}

function snakeToPascal(s: string) {
	return s.toLowerCase().split('_').map(capitalize).join('');
}

function capitalize(s: string) {
	return s[0].toUpperCase() + s.slice(1);
}

void main()
	.then(() => console.log('[INFO] All schemas generated !'))
	.catch((err) => {
		console.error('[ERROR]', err);
		process.exit(1);
	});
