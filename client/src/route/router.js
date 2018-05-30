import Vue from 'vue'
import VueRouter from 'vue-router'

//Pages
import IndexPage from '.././pages/IndexPage.vue'
import Login from '.././pages/Login.vue'
import Logout from '.././pages/Logout.vue'
import CreateAppeal from '.././pages/Appeal/Create.vue'
import AppealList from '.././pages/Appeal/AppealList.vue'
import AppealCategory from '.././pages/Appeal/AppealCategory.vue'
import Register from '.././pages/Register.vue'
import UserProfile from '.././pages/User/ViewProfile.vue'
import NotFound from '.././pages/404.vue'
import Session from '.././pages/livestream/Session.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: "/",
    component: IndexPage
  },

  {
    path: "/login", 
    component: Login,
  },

  {
    path: "/register", 
    component: Register,
  },

  {
    path: "/appeals", 
    component: AppealList
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
    path: "/appeal/create",
    component: CreateAppeal
  },
  
  {
    path: "/logout", 
    component: Logout
  },

  {
    path: "/profile/:username",
    component: UserProfile
  },

  {
    path: "/session",
    component: Session
  },

  {
    path: "/404",
    component: NotFound
  },

  { 
    path: "*",
    redirect: "/404"
  }
]

// Export Router back to main.js
export const router = new VueRouter({
  mode: "history",
  routes
})