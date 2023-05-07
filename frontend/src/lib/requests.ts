import { API_BASE_URL, log } from '.';

import type { AxiosRequestConfig } from 'axios';
import axios from 'axios';

import type { Quizoot } from '@interfaces/quizoot';

const quizootApi = axios.create({
    baseURL: API_BASE_URL,
    timeout: 1000,
    maxBodyLength: 2000,
    xsrfHeaderName: 'X-CSRFTOKEN',
    xsrfCookieName: 'csrftoken',
});

export type ApiResponse =
    | Quizoot.Quiz
    | Quizoot.Quiz[]
    | Quizoot.Question
    | Quizoot.Question[];

export async function makeRequest<TData extends ApiResponse>(
    requestConfig: AxiosRequestConfig
): Promise<TData> {
    try {
        const response = await quizootApi(requestConfig);
        return response.data;
    } catch (err) {
        if (axios.isAxiosError(err)) {
            // TODO: display
        }
        const method = requestConfig.method ?? 'GET';
        log(`Could not ${method} to ${requestConfig.url}:\n`, err);
        throw new Error(`Could not ${method} to ${requestConfig.url}`);
    }
}
