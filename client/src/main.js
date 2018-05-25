import Vue from 'vue'
import Vuetify from 'vuetify'
import 'vuetify/dist/vuetify.min.css'
import Router from 'vue-router'

import App from './App.vue'
import VueRouter from 'vue-router';

import Login from './pages/Login.vue'
import Logout from './pages/Logout.vue'
import Appeal from './pages/Appeal/Appeal.vue'
import AppealCategory from './pages/Appeal/AppealCategory.vue'
import Register from './pages/Register.vue'

Vue.use(Vuetify)
Vue.use(Router)

const routes = [
  {
    path: "/login", 
    component: Login,
  },

  {
    path: "/register", 
    component: Register,
  },

  {
    path: "/appeal", 
    component: Appeal
  },

  {
    path: "/appeal/category/:categName/", 
    component: AppealCategory
  },

  {
    path: "/appeal/category/:categName/:subcategName", 
    component: AppealCategory
  },
  
  {
    path: "/logout", 
    component: Logout
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
