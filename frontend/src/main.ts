import App from '@/App.vue';
import {createApp} from 'vue';
import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome';
import '@/scripts/font_awesome_icons';

createApp(App)
    .component('font-awesome-icon', FontAwesomeIcon)
    .mount('#app');
