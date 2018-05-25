import Vue from 'vue'
import Vuetify from 'vuetify'
import 'vuetify/dist/vuetify.min.css'
import Router from 'vue-router'

import App from './App.vue'
import VueRouter from 'vue-router';

import Login from './pages/Login.vue'
import Appeal from './pages/Appeal/Appeal.vue'
import AppealCategory from './pages/Appeal/AppealCategory.vue'

Vue.use(Vuetify)
Vue.use(Router)

const routes = [
  {
    path: "/login", component: Login
  },

  {
    path: "/appeal", component: Appeal
  },

  {
    path: "/appeal/category/:categName", component: AppealCategory
  }
]

const router = new VueRouter({
  mode: "history",
  routes
})

new Vue({
  el: '#app',
  render: h => h(App),
  router
})
