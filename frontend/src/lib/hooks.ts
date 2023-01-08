import { ref } from 'vue';
import type { Ref } from 'vue';
import type { AxiosRequestConfig } from 'axios';

import { makeRequest } from '@/lib/requests';
import type { ApiResponse } from '@/lib/requests';

export interface FetchResponse<T> {
    data: Ref<T | null>;
    error: Ref;
    isFetching: Ref<boolean>;
}

type Options = Omit<AxiosRequestConfig, 'url'>;

export async function useFetch<TData extends ApiResponse>(
    url: string,
    options?: Options
): Promise<FetchResponse<TData>> {

    const state: FetchResponse<TData> = {
        data: ref(null),
        error: ref(null),
        isFetching: ref(true),
    };

    async function fetchData() {
        try {
            state.data.value = await makeRequest<TData>({
                url,
                ...options,
            });
        } catch (error) {
            state.error.value = error;
        } finally {
            state.isFetching.value = false;
        }
    }

    await fetchData();

    return state;
}
