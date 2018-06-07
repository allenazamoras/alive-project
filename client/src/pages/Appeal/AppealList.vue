<template>
  <div>
    <app-nav/>
  
    <v-container grid-list-xl>
      <v-layout justify-center row>
          <v-flex>
            <v-layout row wrap v-if="appeals.length > 0" v-for="(appeal, index) in appeals" :key="`appeal-${index}`" justify-center :class="{'pt-3': index > 0}">
              <v-flex xs12 sm12 md8 lg6>
                <appeal-view :appeal="appeal" :promptDialog.sync="promptDialog"/>
              </v-flex>
            </v-layout>
        </v-flex>
      </v-layout>   
    </v-container>

    <notifications :promptDialog.sync="promptDialog"/>
    <snackbar :snackbar="snackbar"/>
  </div>
  
</template>

<script>
import appNav from '../.././components/AppNav'
import snackbar from '../../components/Snackbar'
import notifications from '../../components/Notifications'
import appealView from '../../components/AppealView'

import moment from 'moment'
import axios from 'axios'
import {mapGetters, mapMutations} from 'vuex'

export default {
  data() { 
    return { 
      promptDialog: false,
      snackbar: {},
      
      pk: -1,

      //single appeal component variables
      cancel: false,

      categories: [
        {name: "School", url: "/appeal/category/school", img: "https://picsum.photos/200/300/?random"},
        {name: "Work", url: "/appeal/category/work", img: "https://picsum.photos/200/300/?random"},
        {name: "Family", url: "/appeal/category/family", img: "https://picsum.photos/200/300/?random"},
        {name: "Relationships", url: "/appeal/category/others", img: "https://picsum.photos/200/300/?random"},
        {name: "Others", url: "/appeal/category/others", img: "https://picsum.photos/200/300/?random"},
      ],

      appeals: []
    }
  },

  computed: { 
    ...mapGetters('userModule', [
      'getConfig'
    ])
  },

  created() { 
    axios.get(`${process.env.API_URL}/request/?page=1`, this.getConfig)
    .then((res) => { 
      this.appeals = res.data.results
      console.log(this.appeals)
    })
  },

  components: { 
    appNav,
    snackbar,
    notifications,
    appealView
  }
}
</script>
