<template>
  <div>
    <v-container>
      <appeal-view :appeal="appeal"/>
    </v-container>
    
  </div>
</template>

<script>
import axios from 'axios'
import appealView from '../../components/AppealView'

export default {
  data() { 
    return { 
      appeal: {}
    }
  },

  components: { 
    appealView
  },

  created() { 
    axios.get(`${process.env.API_URL}/request/62/single_appeal/`, this.getConfig)
    .then((res) => { 
      this.appeal = res.data
      console.log(this.appeal)
    })
  }
}
</script>
