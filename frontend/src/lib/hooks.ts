import { ref, watch } from 'vue';

import type { ApiResponse } from '@/lib/requests';
import type { AxiosRequestConfig } from 'axios';
import type { Ref } from 'vue';
import { makeRequest } from '@/lib/requests';

export interface FetchResponse<T> {
    data: Ref<T | null>;
    error: Ref;
    isFetching: Ref<boolean>;
}

type Options = Omit<AxiosRequestConfig, 'url'>;

export function useFetch<TData extends ApiResponse>(
    url: string,
    options?: Options
): FetchResponse<TData> {
    const state: FetchResponse<TData> = {
        data: ref(null),
        error: ref(null),
        isFetching: ref(true),
    };

    async function fetchData() {
        makeRequest<TData>({ url, ...options })
            .then((data) => {
                state.data.value = data;
            })
            .catch((error) => {
                state.error.value = error;
            })
            .finally(() => {
                state.isFetching.value = false;
            });
    }

    fetchData();

    return state;
}
