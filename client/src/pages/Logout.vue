<template>  
  <div>

  </div>
</template>

<script>
export default {
  beforeCreate() { 
    localStorage.removeItem("token")
    this.$store.commit("setUsername", "")
    this.$router.push("/")
  }
}
</script>