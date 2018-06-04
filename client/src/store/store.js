import Vue from 'vue'
import Vuex from 'vuex'
import persistedState from 'vuex-persistedstate'

//Modules
import userModule from './user/userModule'
import sessionModule from './session/sessionModule'

Vue.use(Vuex)

export const store = new Vuex.Store({
  modules: {
    userModule,
    sessionModule
  },

  plugins: [persistedState()],
})