<template>
  <v-container>
    {{ category }} category
  </v-container>
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
