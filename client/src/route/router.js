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

import {store} from '.././store/store.js'

Vue.use(VueRouter)

const isLoggedIn = () => store.getters.getUsername.length > 0 ? true : false
const firstToUpper = (string) => string.charAt(0).toUpperCase() + string.slice(1)

const routes = [
  {
    name: "Home",
    path: "/",
    component: IndexPage,
    meta: { 
      title: "Home"
    }
  },

  {
    name: "Login",
    path: "/login", 
    component: Login,
    meta: { 
      title: "Login"
    }
  },

  {
    name: "Register",
    path: "/register", 
    component: Register,
    meta: { 
      title: "Register"
    }
  },

  {
    path: "/appeals", 
    component: AppealList,
    meta: { 
      title: "Appeals"
    }
  },

  {
    name: "Category",
    path: "/appeal/category/:categName/", 
    component: AppealCategory,
    beforeEnter: (to, from, next) => { 
      let title = to.params.categName
      document.title = firstToUpper(title)
    }
  },

  {
    name: "Subcategory",
    path: "/appeal/category/:categName/:subCategName", 
    component: AppealCategory,
    beforeEnter: (to, from, next) => { 
      let title = to.params.subCategName
      document.title = firstToUpper(title)
    }
  },

  {
    name: "Create",
    path: "/appeal/create",
    component: CreateAppeal,
    meta: { 
      title: "Create"
    }
  },
  
  {
    name: "Logout",
    path: "/logout", 
    component: Logout
  },

  {
    path: "/profile/:username",
    component: UserProfile
  },

  {
    name: "Session",
    path: "/session",
    component: Session,
    beforeEnter: (to, from, next) => { 
      console.log(store.state.session.appealID)
        if(store.state.session.appealID > 0) { 
          next()  
        } else { 
          next({path: from.path})
        }
    }
  },

  {
    name: "404",
    path: "/NotFound",
    component: NotFound,
    meta: { 
      title: "404 - Not Found"
    }
  },

  {
    path: "*",
    redirect: "/NotFound"
  }
]

// Export Router back to main.js
export const router = new VueRouter({
  mode: "history",
  routes
})

router.beforeEach((to, from, next) => { 
  // if(to.name == "Login" || to.name == "Register" || to.name == "Home") { 
  //   if(isLoggedIn())
  //     next("/")
  //   else
  //     next()
  // } else { 
  //   if(!isLoggedIn()) { 
  //     next({name: "Login"})
  //   }
  // }

  if(to.meta.title) { 
    document.title = to.meta.title
  }

  next()
})