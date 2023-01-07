import { ref } from 'vue';
import type { Ref } from 'vue';
import type { AxiosRequestConfig } from 'axios';
import { makeRequest } from '@/lib/requests';
import type { ApiResponse } from '@/lib/requests';

export interface UseFetchReturn<T> {
    data: Ref<ApiResponse | null>;
    error: Ref;
    isFetching: Ref<boolean>;
}

type UseFetchOptions = Omit<AxiosRequestConfig, 'url'>;

export async function useFetch<T>(
    url: string,
    options?: UseFetchOptions
): Promise<UseFetchReturn<T>> {

    const state: UseFetchReturn<T> = {
        data: ref(null),
        error: ref(null),
        isFetching: ref(true),
    }

    async function fetchData() {
        try {
            state.data.value = await makeRequest<ApiResponse>({
                url,
                ...options
            });
        } catch(error) {
            state.error.value = error;
        } finally {
            state.isFetching.value = false;
        }
    }

    await fetchData();

    return state
}
