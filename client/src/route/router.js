import Vue from 'vue'
import VueRouter from 'vue-router'

//Pages
import UserIndex from '.././pages/IndexPage.vue'
import VisitorIndex from '.././pages/VisitorIndex.vue'
import Login from '.././pages/Login.vue'
import Logout from '.././pages/Logout.vue'
import CreateAppeal from '.././pages/Appeal/Create.vue'
import AppealList from '.././pages/Appeal/AppealList.vue'
import AppealCategory from '.././pages/Appeal/AppealCategory.vue'
import Register from '.././pages/Register.vue'
import UserProfile from '.././pages/User/ViewProfile.vue'
import NotFound from '.././pages/404.vue'
import Session from '.././pages/livestream/Session.vue'

import {store} from '.././store/store'

Vue.use(VueRouter)

const firstToUpper = (string) => string.charAt(0).toUpperCase() + string.slice(1)

const auth = (to, from, next) => { 
  if(store.getters['userModule/isLoggedIn']) { 
    next()
  } else { 
    next({name: "Login"})
  }
}

const routes = [
  {
    name: "Home",
    path: "/",
    component: (store.getters['userModule/isLoggedIn']) ? UserIndex: VisitorIndex,
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
    }, 

    beforeEnter: (to, from, next) => { 
      if(store.getters['userModule/isLoggedIn']) { 
        next(false)
      } else { 
        next()
      }
    }
  },

  {
    name: "Logout",
    path: "/logout", 
    component: Logout
  },

  {
    name: "Register",
    path: "/register", 
    component: Register,
    meta: { 
      title: "Register"
    },

    beforeEnter: (to, from, next) => { 
      if(store.getters['userModule/isLoggedIn']) { 
        next(false)
      } else { 
        next()
      }
    }
  },

  {
    path: "/appeals", 
    component: AppealList,
    meta: { 
      title: "Appeals"
    },
    beforeEnter: auth
  },

  {
    name: "Category",
    path: "/appeal/category/:categName/", 
    component: AppealCategory,
    beforeEnter: (to, from, next) => { 
      if(store.getters['userModule/isLoggedIn']) { 
        let title = to.params.categName
        document.title = firstToUpper(title)
        next()
      } else { 
        next({name: "Login"})
      }
    }
  },

  {
    name: "Subcategory",
    path: "/appeal/category/:categName/:subCategName", 
    component: AppealCategory,
    beforeEnter: (to, from, next) => { 
      if(store.getters['userModule/isLoggedIn']) { 
        let title = to.params.subCategName
        document.title = firstToUpper(title)
        next()
      } else { 
        next({name: "Login"})
      }
    }
  },

  {
    name: "Create",
    path: "/appeal/create",
    component: CreateAppeal,
    meta: { 
      title: "Create"
    },
    beforeEnter: auth
  },

  {
    path: "/profile/:username",
    component: UserProfile,
    beforeEnter: auth
  },

  {
    name: "Session",
    path: "/session",
    component: Session,
    beforeEnter: (to, from, next) => { 
      if(store.getters['userModule/isLoggedIn']) { 
        if(store.state.sessionModule.appealID > 0) { 
          next()  
        } else { 
          next({path: from.path})
        }
      } else { 
        next({name: "Login"})
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