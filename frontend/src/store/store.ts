import type { InjectionKey } from 'vue';
import { createStore, useStore as baseUseStore } from 'vuex';
import type { Store as BaseStore, CommitOptions } from 'vuex';
import { state } from '@/store/state';
import type { State } from '@/store/state';
import { mutations } from '@/store/mutations';
import type { Mutations } from '@/store/mutations';

export const store = createStore({
    state,
    // getters,
    mutations,
});

export const key: InjectionKey<BaseStore<State>> = Symbol();

export type Store = Omit<BaseStore<State>, 'getters' | 'commit'> & {
    commit<K extends keyof Mutations, P extends Parameters<Mutations[K]>[1]>(
        key: K,
        payload: P,
        options?: CommitOptions
    ): ReturnType<Mutations[K]>;
};

export function useStore() {
    return baseUseStore(key);
}
