import Vue from 'vue'
import Vuex from 'vuex'
import persistedState from 'vuex-persistedstate'

Vue.use(Vuex)

export const store = new Vuex.Store({
  state: { 
    user: {
      username: "",
      userID: -1,
      profilePic: "",
      fullName: "",

      snackbar: false,
      timeout: 3000,
    }
  },

  plugins: [persistedState()],

  mutations: {
    setUserAll(state, user) { 
      state.user = user
    },

    setSnackbarState(state, boolean) {
      state.snackbar = boolean
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

    getSnackbarState(state) { 
      return state.snackbar
    },

    getSnackbarTimeout(state) { 
      return state.timeout
    }
  }
})