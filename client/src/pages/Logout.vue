<template>  
  <div>

  </div>
</template>

<script>
export default {
  beforeCreate() { 
    localStorage.removeItem("token")
    this.$router.push("/")
  }
}
</script>