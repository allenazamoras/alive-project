<template>
  <div>
    <app-nav/>
    <nuxt/>
  </div>
</template>

<script>
import appNav from '~/components/appnav'

export default {
  components: {
    appNav
  }
}
</script>

<style>
  nav { 
    margin-bottom : 10vh;
  }
</style>
