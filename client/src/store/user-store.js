export default {
  namespaced: true,
  state: {
    user: { 
      username: "",
      userID: -1,
      profilePic: "",
      fullName: "",
    },

    config: { 
      headers: { 
        Authorization: ""
      }
    }

  },

  getters: {
    getUsername: (state) => state.user.username,
    getUserID: (state) => state.user.userID,
    getUserData: (state) => state.user,
    getConfig: (state) => state.config
  },

  mutations: {
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
}