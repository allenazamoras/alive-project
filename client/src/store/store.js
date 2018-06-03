import Vue from 'vue'
import Vuex from 'vuex'
import persistedState from 'vuex-persistedstate'

//Modules
import userModule from './user/userModule'

Vue.use(Vuex)

export const store = new Vuex.Store({
  modules: {
    userModule
  },  

  state: { 
    user: {
      username: "michael",
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