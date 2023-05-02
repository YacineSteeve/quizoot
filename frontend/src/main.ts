import App from '@/App.vue';
import { createApp } from 'vue';
import router from '@/router';
import '@jsonforms/vue-vanilla/vanilla.css';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import '@/lib/init_font_awesome';

createApp(App)
    .use(router)
    .component('font-awesome-icon', FontAwesomeIcon)
    .mount('#app');
