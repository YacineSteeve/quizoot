import App from '@/App.vue';
import {createApp} from 'vue';
import router from '@/scripts/router';
import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome';
import '@/scripts/font_awesome_icons';

createApp(App)
    .use(router)
    .component('font-awesome-icon', FontAwesomeIcon)
    .mount('#app');
