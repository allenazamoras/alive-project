<template>
  <div>
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
            loading="true"
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
      this.$router.push(`/search/${this.searchText}`)
    },

    query() { 
      // console.log
      if(this.$route.params.searchText.length > 0) { 
        axios.get(`${process.env.API_URL}/search?search=${this.$route.params.searchText}&page=1/`, this.getConfig)
        .then((res) => { 
          this.results = res.data.results
        })
      }
    }
  },

  watch: { 
    '$route' (to, from) { 
      this.query()
    }
  },

  created() { 
    this.query()
  }
}
</script>