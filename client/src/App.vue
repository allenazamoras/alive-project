<template>
  <v-app>
    <main>
      <v-content>
        <router-view></router-view>
      </v-content>
      
    </main>
      
    
  </v-app>
</template>

<script>
import appNav from './components/AppNav.vue'
import subNav from './components/SubNav.vue'

export default {
  name: 'app',
  data () {
    return {
      msg: 'Welcome to Your Vue.js App'
    }
  },

  components: { 
    appNav,
    subNav
  },
}
</script>

