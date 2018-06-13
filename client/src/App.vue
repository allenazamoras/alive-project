<template>
  <v-app class="grey lighten-3">
    <app-nav v-if="isLoggedIn"/>
    <main app>
      <v-content>
        <router-view></router-view>
        <snackbar/>
      </v-content>
    </main>
  </v-app>
</template>

<script>
import appNav from './components/AppNav.vue'
import snackbar from './components/Snackbar.vue'

import {mapGetters} from 'vuex'

export default {
  data () {
    return {
    }
  },
  components: { 
    appNav,
    snackbar
  },
  computed: { 
    ...mapGetters('userModule', [
      'isLoggedIn'
    ])
  },
  name: 'App'
}
</script>
