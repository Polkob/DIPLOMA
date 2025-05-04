import './assets/main.css'
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import { createApp } from 'vue'
import router from './router/router'
import App from './App.vue'
import Toast, { POSITION } from "vue-toastification";
import 'vue-toastification/dist/index.css'

const vuetify = createVuetify({
    components,
    directives,
  })

createApp(App).use(vuetify).use(router).use(Toast, {
  position: POSITION.BOTTOM_CENTER, 
  timeout: 3000,
  closeOnClick: true,
  pauseOnHover: true,
  draggable: true,
}).mount('#app')
