import Vue from 'vue'
import Router from 'vue-router'

//Pages
import UserIndex from '.././pages/IndexPage.vue'
import VisitorIndex from '.././pages/VisitorIndex.vue'
import Login from '.././pages/Login.vue'
import Logout from '.././pages/Logout.vue'
import AppealList from '.././pages/Appeal/AppealList.vue'
import AppealCategory from '.././pages/Appeal/AppealCategory.vue'
import Register from '.././pages/Register.vue'
import UserProfile from '.././pages/User/ViewProfile.vue'
import EditProfile from '.././pages/User/EditProfile.vue'
import NotFound from '.././pages/404.vue'
import Session from '.././pages/livestream/Session.vue'
import Search from '.././pages/Search'
import SingleAppeal from '../pages/Appeal/SingleAppeal'

import store from '../store/store'

const firstToUpper = (string) => string.charAt(0).toUpperCase() + string.slice(1)

const auth = (to, from, next) => {
  if (store.getters['userModule/isLoggedIn']) {
    next()
  } else {
    next({name: 'Login'})
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
    path: "/appeals/list", 
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
    name: "Search",
    path: "/search/:searchText",
    component: Search,
    beforeEnter: auth
  },

  {
    name: "SearchBlank",
    path: "/search",
    component: Search,
    beforeEnter: auth
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
    path: "/settings",
    component: EditProfile,
    beforeEnter: auth
  },

  {
    path: "/profile/:username",
    component: UserProfile,
    beforeEnter: auth
  },

  {
    path: "/appeal/:id",
    component: SingleAppeal,
    beforeEnter: auth
  },

  {
    name: "Session",
    path: "/session/:id",
    component: Session,
    beforeEnter: (to, from, next) => { 
      if(store.getters['userModule/isLoggedIn']) { 
        next()
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

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes
})