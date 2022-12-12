import { API_BASE_URL, log } from '.';

import type { AxiosRequestConfig } from 'axios';
import axios from 'axios';

const quizootApi = axios.create({
    baseURL: API_BASE_URL,
    timeout: 1000,
    maxBodyLength: 2000,
});

export type ApiResponse =
    | number
    | string
    | boolean
    | null
    | ApiResponse[]
    | { [x: string]: ApiResponse };

export async function makeRequest<TData extends ApiResponse>(
    config: AxiosRequestConfig
): Promise<TData> {
    try {
        const response = await quizootApi(config);
        return response.data;
    } catch (err) {
        if (axios.isAxiosError(err)) {
            // TODO: display
        }
        const method = config.method ?? 'GET';
        log(`Could not ${method} to ${config.url}:\n`, err);
        throw new Error(`Could not ${method} to ${config.url}`);
    }
}
