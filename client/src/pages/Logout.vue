<template>  
  <div>

  </div>
</template>

<script>
import {mapActions} from 'vuex'

export default {
  methods: {
    ...mapActions('userModule', [
      'removeUserData'
    ]),
  },
  
  created() {
    localStorage.removeItem("token")
    this.removeUserData()
    window.location.replace("/")
  }
}
</script>