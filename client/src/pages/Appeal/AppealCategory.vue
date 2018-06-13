<template>
  <div>
    <v-container>
      {{ category }} category
    </v-container>
  </div>
  
</template>

<script>

export default {
  data() { 
    return { 
      category: ""
    }
  },
  created() { 
    this.category = this.$route.params
  }
}
</script>
