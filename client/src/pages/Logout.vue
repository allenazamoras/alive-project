<template>  
  <div>

  </div>
</template>

<script>
export default {
  beforeCreate() { 
    localStorage.removeItem("token")
    this.$store.dispatch("removeUserData")
    this.$router.push("/")
  }
}
</script>