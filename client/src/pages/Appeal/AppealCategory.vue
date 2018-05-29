<template>
  <div>
    <app-nav/>
    <v-container>
      {{ category }} category
    </v-container>
  </div>
  
</template>

<script>
import appNav from '../.././components/AppNav.vue'

export default {
  data() { 
    return { 
      category: ""
    }
  },
  created() { 
    this.category = this.$route.params
  },

  components: { 
    appNav
  }
}
</script>
