import Vue from 'vue'
import Vuex from 'vuex'
import persistedState from 'vuex-persistedstate'
import userModule from './user/userModule'
import dialogModule from './dialog/dialogModule'

Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    userModule,
    dialogModule
  },
  plugins: [persistedState()],
})