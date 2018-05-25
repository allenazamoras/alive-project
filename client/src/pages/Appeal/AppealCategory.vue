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

    axios.get("user/dicksSucked")
    .then((res)=> { 
      this.dicksSucked = res.data.dicksSucked
    })
  }
}
</script>
