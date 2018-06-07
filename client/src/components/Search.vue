<template>
  <div>
    <v-container>
      <v-text-field
          v-model="searchText"
          flat
          solo-inverted
          prepend-icon="search"
          label="Search"
          class="hidden-sm-and-down"
          @keyup="query"
      >
      </v-text-field>
    </v-container>
  </div>
</template>

<script>
import axios from 'axios'
import {mapGetters} from 'vuex'

export default {
  data() { 
    return { 
      results: [],
      timer: null,
      searchFlag: false,
      searchText: ""
    }
  },

  methods: { 
    query() { 
      this.timer = setTimeout(() => {
        if(this.searchText.length > 0) { 
          axios.get(`${process.env.API_URL}/search?search=${this.searchText}&page=1`, this.getConfig)
          .then((res) => { 
            this.results = res.data
          })
        } else { 
          this.results = []
        }
      }, 500)
    },

    toTrue() { 
      console.log("querying")
      console.log(`${process.env.API_URL}/search?search=${this.searchText}`)
      
    }
  },

  computed: { 
    ...mapGetters('userModule', [
      'getConfig'
    ])
  }
}
</script>