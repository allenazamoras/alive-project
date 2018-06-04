<template>
  <div>
    <app-nav/>
    <v-container>
      index page
    </v-container>
  </div>
</template>

<script>
import appNav from '../components/AppNav.vue'
import {mapState} from 'vuex'

export default {
  data() { 
    return { 
      // test: ""
    }
  },

  computed: { 

  },

  methods: { 

  },

  created() { 
    
  },

  components: { 
    appNav
  }  
}
</script>
