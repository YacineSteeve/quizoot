import App from '@/App.vue';
import { createApp } from 'vue';
import router from '@/router';
import { store, key } from './store/store';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import '@/lib/init_font_awesome';

createApp(App)
    .use(router)
    .use(store, key)
    .component('font-awesome-icon', FontAwesomeIcon)
    .mount('#app');
