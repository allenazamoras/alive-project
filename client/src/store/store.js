import Vue from 'vue'
import Vuex from 'vuex'
import persistedState from 'vuex-persistedstate'

Vue.use(Vuex)

export const store = new Vuex.Store({
  state: { 
    username: "",
  },

  plugins: [persistedState()],

  mutations: { 
    setUsername(state, username) { 
      state.username = username
    },
  },

  actions: { 
    setUsername(state, username) { 
      if(state.username.length == 0) { 
        context.commit("setUsername", username)
      }
    }
  },

  getters: { 
    getUsername(state) { 
      return state.username
    }
  }
})