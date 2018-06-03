<template>
  <div>
    <app-nav/>
    <v-container>
      index page

    {{say()}}
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
    localComputed() { 

    },

    ...mapState('userModule', [
      'string'
    ]),
  },

  methods: { 
    say() { 
      console.log(this.string)
    }
  },

  created() { 
    // this.test = this.$store.
  },

  components: { 
    appNav
  }  
}
</script>
