import Vue from 'vue'
import Vuex from 'vuex'
import persistedState from 'vuex-persistedstate'

//Modules
// import navbar from './navbar-store.js'

Vue.use(Vuex)

export const store = new Vuex.Store({
  state: { 
    user: {
      username: "",
      userID: -1,
      profilePic: "",
      fullName: "",

      config: { 
        headers: { 
          Authorization: "",
        }
      }
    },

    session: { 
      appealID: -1,
      sessionID: "",
      tokenID: "",
    }
  },

  plugins: [persistedState()],

  mutations: {
    setUserAll(state, user) { 
      state.user = user
    },

    setSession(state, session) { 
      state.session = session
    }
  },

  actions: {
    setUserData({commit}, user) { 
      commit("setUserAll", user)
    },

    removeUserData({commit})  {
      const user = {
        username: "",
        userID: -1,
        profilePic: "",
        fullName: ""
      }

      commit("setUserAll", user)
    }
  },

  getters: { 
    getUsername(state) { 
      return state.user.username
    },

    getUserID(state) { 
      return state.user.userID
    },

    getUserData(state) { 
      return state.user
    },

    getConfig: (state) => state.user.config
  }
})