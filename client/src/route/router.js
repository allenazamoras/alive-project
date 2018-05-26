import Vue from 'vue'
import VueRouter from 'vue-router'

//Pages
import Login from '.././pages/Login.vue'
import Logout from '.././pages/Logout.vue'
import Appeal from '.././pages/Appeal/Appeal.vue'
import AppealCategory from '.././pages/Appeal/AppealCategory.vue'
import Register from '.././pages/Register.vue'
import UserProfile from '.././pages/User/ViewProfile.vue'

Vue.use(VueRouter)

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
  },

  {
    path: "/profile/:username",
    component: UserProfile
  }
]

// Export Router back to main.js
export const router = new VueRouter({
  mode: "history",
  routes
})