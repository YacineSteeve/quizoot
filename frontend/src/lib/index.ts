// Check the environnement mode: DEV or PROD ?
export const isDev = () => import.meta.env.DEV;

const PORT = import.meta.env.VITE_QUIZOOT_SERVER_PORT ?? '8000';

export const API_BASE_URL = `http://localhost:${PORT}`;

export const log = (...data: any[]) => {
    if (isDev()) {
        console.log('[QUIZOOT DEV]', ...data);
    }
};
