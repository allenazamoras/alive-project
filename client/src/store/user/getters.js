const getters = { 
  getUserData: (state) => {
    const user = { 
      username: state.username,
      userID: state.userID,
      profilePic: state.profilePic,
      fullName: state.fullName,
    }

    return user
  },    

  getConfig: (state) => state.config,
  isLoggedIn: (state) => (state.username.length > 0) ? true: false
}

export default getters