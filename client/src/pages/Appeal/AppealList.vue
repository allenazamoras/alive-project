<template>
  <div>
    <v-container grid-list-xl>
      <v-layout justify-center row>
        <v-flex xs12 sm9 md8 lg6>
          <v-layout
            row
            wrap
            justify-center
          >
          <v-flex xs12 class="text-xs-center">
          </v-flex>
          </v-layout>

          <v-layout 
            row 
            wrap 
            v-if="appeals.length > 0" 
            v-for="(appeal, index) in appeals" 
            :key="`appeal-${index}`" 
            justify-center 
            :class="{'pt-3': index > 0}"
          >
            <v-flex 
              xs12
            >
              <appeal-view :appeal="appeal"/>
            </v-flex>
            <v-flex 
              xs12
              v-if="index == appeals.length - 1"
              text-xs-center
            >
              <v-pagination 
                prev-icon="arrow_left" 
                next-icon="arrow_right"
                :length="totalPages" 
                v-model="currentPage"
              ></v-pagination>
            </v-flex>
          </v-layout>

          <v-layout
            row
            justify-center
            v-if="appeals.length == 0"
          >
            There's nothing here.
          </v-layout>
        </v-flex>
      </v-layout>   
    </v-container>
  </div>
  
</template>

<script>
import appealView from '../../components/AppealView'

import moment from 'moment'
import axios from 'axios'
import {mapGetters, mapMutations} from 'vuex'

export default {
  data() { 
    return { 
      snackbar: {},
      
      pk: -1,
      currentPage: 1,
      totalPages: 1,

      timer: null,

      //spinner for loadNew button
      loadNewLoading: false,

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
  components: { 
    appealView
  },
  computed: { 
    ...mapGetters('userModule', [
      'getConfig'
    ])
  },
  methods: { 
    loadNew() { 
      this.loadNewLoading = true
    },
    getAppeals() {
      axios.get(`${process.env.API_URL}/request/?page=${this.currentPage}`, this.getConfig)
      .then((res) => { 
        this.appeals = res.data.results
      })

      setTimeout(this.getAppeals, 5600)
    }
  },
  watch: { 
    'currentPage' () { 
      axios.get(`${process.env.API_URL}/request/?page=${this.currentPage}`, this.getConfig)
      .then((res) => { 
        this.appeals = res.data.results
      })
    }
  },
  created() { 
    this.getAppeals()
  },
  beforeRouteLeave(to, from, next) { 
    clearTimeout(this.timer)
    next()
  }
}
</script>
