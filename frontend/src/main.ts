import App from '@/App.vue';
import { createApp } from 'vue';
import router from '@/views/router';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import '@/lib/init_font_awesome';

createApp(App)
    .use(router)
    .component('font-awesome-icon', FontAwesomeIcon)
    .mount('#app');
