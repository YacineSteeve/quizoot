import { URL, fileURLToPath } from 'node:url';
import { defineConfig, loadEnv } from 'vite';

import vue from '@vitejs/plugin-vue';
import vueJsx from '@vitejs/plugin-vue-jsx';

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => {
    const env = loadEnv(mode, process.cwd());
    const PORT = env.VITE_QUIZOOT_SERVER_PORT ?? '8000';

    return {
        plugins: [vue(), vueJsx()],
        resolve: {
            alias: {
                '@': fileURLToPath(new URL('./src', import.meta.url)),
                '@interfaces': fileURLToPath(new URL('../interfaces', import.meta.url)),
            },
        },
        server: {
            proxy: {
                '/api': {
                    target: `http://localhost:${PORT}`,
                    changeOrigin: true,
                },
            },
        },
    };
});
