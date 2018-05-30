<template>
  <div>
    <app-nav/>
    <v-container grid-list-lg>
      <!-- <v-layout justify-center row>
        <v-flex lg7>
          <v-subheader class="pl-0">Categories</v-subheader>
          <v-layout row wrap>
            <v-flex xs12 sm3 md2 lg3 v-for="(category, index) in categories" :key="`category-${index}`">
              <v-card 
                hover
                :to="category.url"
                >
                <v-card-media 
                  :src="category.img"
                  height="90px">

                  <v-card-title primary-title>
                    <h3 class="drop-shadow white--text">{{ category.name }}</h3>
                </v-card-title>
                </v-card-media>
              </v-card>
            </v-flex>
          </v-layout>  -->
          
          <v-layout wrap justify-center>
            <v-flex xs12>
              <v-subheader class="pl-0">Most Recent Appeals</v-subheader>
            </v-flex>
            <v-layout row>
              <v-flex xs12 sm12 md12>
                <v-card class="elevation-3">
                  <v-list three-line>
                    <div v-for="(appeal, index) in appeals" :key="`appeal-${index}`">
                      {{appeal}}
                      <v-list-tile>
                        <v-list-tile-avatar>
                          <img :src="appeal.owner.profile_picture" :alt="appeal.owner.username">
                        </v-list-tile-avatar>
                        <v-list-tile-content :to="appeal.url">
                          <v-list-tile-title>
                            {{ appeal.request_title}}
                          </v-list-tile-title>
                          <v-list-tile-sub-title>
                            <span class="text--primary">
                              {{ appeal.username }}
                            </span>
                            {{ appeal.owner.username }} - {{ appeal.detail }} <span class="grey--text text--lighten-1">{{ getMoment(appeal.date_pub) }}</span>
                          </v-list-tile-sub-title>
                        </v-list-tile-content>              
                        <v-list-tile-action>
                          <v-btn depressed slot="activator" @click="toSession(appeal)">
                            <h3><v-icon>video_call</v-icon> Call</h3>
                          </v-btn>
                        </v-list-tile-action>
                      </v-list-tile>
                      <v-divider inset v-show="index < appeals.length - 1"></v-divider>
                    </div>
                    
                  </v-list>
                </v-card>
              </v-flex>
            </v-layout>
          </v-layout>
        </v-flex>
      </v-layout>   
    </v-container>
  </div>
  
</template>

<script>
import moment from 'moment'
import axios from 'axios'

import appNav from '../.././components/AppNav.vue'

export default {
  data() { 
    return { 
      userDialog: false,
      categories: [
        {name: "School", url: "/appeal/category/school", img: "https://picsum.photos/200/300/?random"},
        {name: "Work", url: "/appeal/category/work", img: "https://picsum.photos/200/300/?random"},
        {name: "Family", url: "/appeal/category/family", img: "https://picsum.photos/200/300/?random"},
        {name: "Relationships", url: "/appeal/category/others", img: "https://picsum.photos/200/300/?random"},
        {name: "Others", url: "/appeal/category/others", img: "https://picsum.photos/200/300/?random"},
      ],

      appeals: [

      ]
    }
  },

  methods: {
    getMoment(time) { 
      console.log(time)
      return moment(time, "YYYY-MM-DD hh:mm:ss").fromNow()
    },

    toSession(appeal) { 
      const session = { 
        appealID: appeal.id,
        sessionID: appeal.session_id,
        tokenID: "",
      }

      this.$store.commit("setSession", session)
      this.$router.push("/session")
    }
  },

  created() { 
    axios.get(`${process.env.API_URL}/request/`)
    .then((res) => { 
      this.appeals = res.data
      console.log("data", res)
    })
  },

  components: { 
    appNav
  }
}
</script>

<style>
  .drop-shadow { 
    text-shadow: 0.5px 0.5px #000;
  }
</style>

