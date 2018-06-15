const mutations = { 
  setUserAll(state, user) { 
    state.username = user.username,
    state.userID = user.userID,
    state.profilePic = user.profilePic,
    state.fullName = user.fullName,
    state.config = user.config
  },

  setProfilePic(state, profilePic) { 
    state.profilePic = profilePic
  }
}

export default mutations