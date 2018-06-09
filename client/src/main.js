import Vue from 'vue'
import Vuex from 'vuex'
import VueChatScroll from 'vue-chat-scroll'

// Theme and stylesheet
import Vuetify from 'vuetify'
import 'vuetify/dist/vuetify.min.css'

//Main Vue file
import App from './App.vue'

import {store} from './store/store.js'
import {router} from './route/router.js'

Vue.use(Vuetify)
Vue.use(VueChatScroll)

new Vue({
  el: '#app',
  render: h => h(App),
  router,
  store
})
