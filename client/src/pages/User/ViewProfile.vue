<template>
  <div>
    <app-nav></app-nav>
    <v-container grid-list-lg>
      <v-layout row justify-center align-center>
        <v-flex xs12 sm12 md12 lg8 xl6>
          <v-layout row justify-center align-center>
            <v-flex xs12 sm12 md12 lg12 xl12>
              <v-card tile>
                <v-parallax height="250" :style="`background-image: url(${patternURL}); background-repeat: repeat-x;`">
                  <v-layout row justify-center align-center>
                      <v-flex md12 lg12 sm12 class="text-sm-center">
                        <v-avatar size="80">
                          <img :src="`${user.profile_picture}`" alt="">
                        </v-avatar>
                        <h2 class="grey--text text--darken-3">{{ user.first_name }} {{ user.last_name }}</h2>
                      </v-flex>          
                    </v-layout>
                </v-parallax> 
              </v-card>
            </v-flex>
          </v-layout>

          <v-layout row wrap>
            <v-flex xs12 lg4>
              <v-layout row wrap>
                <v-flex xs12>
                  <v-card>
                    <v-card-text primary-title>
                      <h3>Basic Information</h3>
                      <span>
                        <span class="body-2">Username: </span>{{ user.username }}
                      </span>
                      <br>
                      <span>
                        <span class="body-2">Full Name: </span> {{ user.first_name }} {{ user.last_name }}
                      </span>
                      <br>
                      <span>
                        <span class="body-2">Gender: </span> {{ user.gender }}
                      </span>
                      <br>
                      <span>
                        <!-- <span class="body-2">Joined Date: </span> {{ userInfo.joinedDate }} -->
                      </span>
                    </v-card-text>
                  </v-card>
                </v-flex>

                <!-- <v-flex xs12>
                  <v-card>
                    <v-card-text primary-title>
                      <h3>Awards (2)</h3>
                      <v-tooltip top>
                        <img slot="activator" height="40" :src="`${firstAssist}`" alt="">
                        <span>First assist. Noice!</span>
                      </v-tooltip>
                      <v-tooltip top>
                        <img slot="activator" height="40" :src="`${firstReviewReceived}`" alt="">
                        <span>First Rating Received!</span>
                      </v-tooltip>
                    </v-card-text>
                  </v-card>                  
                </v-flex> -->
              </v-layout>
            </v-flex>

            <v-flex xs12 lg8>
                <v-tabs icons-and-text class="elevation-1">
                  <v-tabs-slider color="black"></v-tabs-slider>
                  <v-tab href="#tab-appeals" v-if="user.openappeals">
                    <!-- <v-icon>fas fa-hands</v-icon> -->
                    Appeals ({{ user.openappeals.length + user.closedappeals.length }})
                  </v-tab>
                  <v-tab href="#tab-assists">
                    Assists ({{ user.offers.openappeals.length + user.offers.closedappeals.length }})
                  </v-tab>
                  <v-tab-item
                    v-for="tab in tabs"
                    :key="tab"
                    :id="'tab-' + tab"
                  >
                    <v-card flat>
                      <appeals :openAppeals="user.openappeals" :closedAppeals="user.closedappeals" v-show="tab == 'appeals'"></appeals>
                      <appeals :openAppeals="user.offers.openappeals" :closedAppeals="user.offers.closedappeals" v-show="tab == 'assists'"></appeals>
                    </v-card>
                  </v-tab-item>
                </v-tabs>
            </v-flex>    
          </v-layout>
        </v-flex>
      </v-layout>
    </v-container>
  </div>
  
</template>

<script>
//Components
import appNav from '../.././components/AppNav.vue'
import appeals from '../.././components/User/Appeals.vue'

//Plugins
import axios from 'axios'
import {mapGetters} from 'vuex'

export default {
  data() { 
    return {
      patternURL: require('../../assets/sun-pattern.png'),
      tabs: ["appeals", "assists"],
      
      //user info 
      user: {},
      viewedUsername: this.$route.params.username,

      //awards
      firstReviewReceived: require("../../assets/achievements/medal.svg"),
      firstAssist: require("../../assets/achievements/badge.svg"),
    }
  },

  methods: { 
    getProfileData() { 
      axios.get(`${process.env.API_URL}/user/${this.$route.params.username}/`, this.getConfig)
      .then((res) => { 
        this.user = res.data
        console.log(res.data.offers.openappeals)
      })
      .catch((err) => { 
        console.log(err)
      })
    }
  },

  computed: { 
    ...mapGetters('userModule', [
      'getConfig'
    ])
  },

  components: { 
    appNav,
    appeals,
  },

  created() {
    this.getProfileData()
  },

  watch: {
    '$route' (to, from) {
      this.getProfileData()
    }
  }
}
</script>