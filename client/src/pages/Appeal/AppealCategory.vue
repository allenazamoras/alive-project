<template>
  <div>

    <v-container grid-list-xl>
      <v-layout
        row
        wrap
      >
        <v-flex xs12 v-for="i in 6">
          <v-card to="/" hover>
            <!-- <appeal-view :appeal="appeal"/> -->
          </v-card>
        </v-flex>
      </v-layout>
    </v-container>
  </div>
  
</template>

<script>
import appealView from '../../components/AppealView'

import axios from 'axios'
import {mapGetters} from 'vuex'

export default {
  data() { 
    return { 
      appeals: [],
    }
  },
  computed: { 
    ...mapGetters('userModule', [
      'getConfig'
    ])
  },
  created() { 
    axios.get(`${process.env.API_URL}/request/list_by_category/`, {
      category_: this.$route.params.id
    }, this.getConfig)
    .then((res) => { 
      console.log(res)
      this.appeals = res
    })
  },

  components: { 
    appealView
  }
}
</script>
