const actions = { 
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
}

export default actions