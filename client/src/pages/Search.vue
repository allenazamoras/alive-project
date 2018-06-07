<template>
  <div>
    <app-nav/>
    <v-container grid-list-xl>
      <v-subheader>Search Results: </v-subheader>
      <v-layout row wrap justify-center>
        <v-flex xs12>
          <v-text-field
            v-model="searchText"
            flat
            solo-inverted
            prepend-icon="search"
            label="Search"
            class="hidden-md-and-up"
            @keyup.enter="search"
          >
          </v-text-field>
        </v-flex>
      </v-layout>

      <v-layout justify-center row wrap v-for="appeal in results" :key="appeal.id">
        <v-flex xs12 md8 lg6>
          <appeal-view :appeal="appeal"/>
        </v-flex>
      </v-layout>
    </v-container>

    <notifications :promptDialog.sync="promptDialog"/>
  </div>
</template>

<script>
import appNav from '../components/AppNav'
import appealView from '../components/AppealView'
import notifications from '../components/Notifications'

import axios from 'axios'
import {mapGetters} from 'vuex'

export default {
  data() { 
    return { 
      searchText: "",
      promptDialog: false,
      results: [],
      timer: null,
      searchFlag: false,
    }
  },

  components: { 
    appNav,
    appealView,
    notifications
  },

  computed: { 
    ...mapGetters('userModule', [
      'getConfig'
    ])
  },

  methods: { 
    search() { 
      if(this.searchText.length > 0) { 
        axios.get(`${process.env.API_URL}/search?search=${this.searchText}&page=1`, this.getConfig)
        .then((res) => { 
          this.results = res.data.results
        })
      }
    }
  },

  watch: { 
    '$route' (to, from) { 
      this.searchText = this.$route.params.searchText
      this.search()
    }
  },

  created() { 
    this.searchText = this.$route.params.searchText
    this.search()
  }
}
</script>