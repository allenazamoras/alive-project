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
      fullName: ""
    }
  },

  plugins: [persistedState()],

  mutations: {
    setUsername(state, username) { 
      state.username = username
    },

    setUserID(state, userID) { 
      state.userID = userID
    },

    setProfilePic(state, profilePic) { 
      state.profilePic = profilePic
    },

    setFullName(state, fullName) { 
      state.fullname = fullName
    },

    setUserAll(state, user) { 
      state.user = user
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
    }
  }
})