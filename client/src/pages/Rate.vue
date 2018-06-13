<template>
  <div>
    <rater :flag="true" :appealID="appealID" :helperName=""/>
  </div>
</template>

<script>
import Rater from '../components/Rating'

export default {
  data() { 
    return { 
      appealID: this.$router.params.id
    }
  },
  components: { 
    Rater
  }  
}
</script>
