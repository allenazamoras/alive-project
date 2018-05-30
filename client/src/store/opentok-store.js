export const opentokSession = {
  // This makes your getters, mutations, and actions accessed by, eg: 'myModule/myModularizedNumber' instead of mounting getters, mutations, and actions to the root namespace.
  namespaced: true,
  state: {
    myModularizedNumber: 0
  },
  getters: {
    myModularizedNumber: state => state.myModularizedNumber
  },
  mutations: {
    setModularizedNumber(state, newNumber) {
      state.myModularizedNumber = newNumber
    }
  }
}