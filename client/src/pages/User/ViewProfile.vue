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
                          <img src="https://randomuser.me/api/portraits/men/1.jpg" alt="">
                        </v-avatar>

                        <h2 class="grey--text text--darken-4">John Doe</h2>
                        <!-- <h4 class="grey--text text--darken-4">@johndoe</h2> -->
                        <h3 class="body-1 grey--text text--darken-4">Programmer | Knee Gore | I want 2 live oh wow</h3>
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
                        <span class="body-2">Username: </span> <router-link to="/">@{{ viewedUsername }}</router-link>
                      </span>
                      <br>
                      <span>
                        <span class="body-2">Full Name: </span> John Doe
                      </span>
                      <br>
                      <span>
                        <span class="body-2">Gender: </span> Male
                      </span>
                      <br>
                      <span>
                        <span class="body-2">Joined Date: </span> May 27, 2018
                      </span>
                    </v-card-text>
                  </v-card>
                </v-flex>

                <v-flex xs12>
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
                </v-flex>
              </v-layout>
            </v-flex>

            <v-flex xs12 lg8>
                <v-tabs icons-and-text centered light class="elevation-1">
                  <v-tabs-slider color="black"></v-tabs-slider>
                  <!-- <v-tab href="#tab-ongoing">
                    Ratings (10)
                    <v-icon color="orange">fas fa-smile</v-icon>
                  </v-tab> -->
                  <v-tab href="#tab-appeals">
                    Appeals (5)
                    <v-icon color="green">fas fa-hands</v-icon>
                  </v-tab>
                  <v-tab href="#tab-assists">
                    Assists (10)
                    <v-icon color="red">fas fa-handshake</v-icon>
                  </v-tab>
                  <v-tab-item
                    v-for="tab in tabs"
                    :key="tab"
                    :id="'tab-' + tab"
                  >
                    <v-card flat>
                      <appeals v-show="currentTab == 'appeals'"></appeals>
                      <assists v-show="currentTab == 'assists'"></assists>
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
import appNav from '../.././components/AppNav.vue'
import appeals from '../.././components/User/Appeals.vue'
import assists from '../.././components/User/Assists.vue'

export default {
  data() { 
    return {
      currentTab: "appeals",
      viewedUsername: this.$route.params.username,
      patternURL: require('../../assets/sun-pattern.png'),
      tabs: [
        "appeals", "assists"
      ],

      firstReviewReceived: require("../../assets/achievements/medal.svg"),
      firstAssist: require("../../assets/achievements/badge.svg")
    }
  },

  methods: { 
    switchTab(tabName) { 
      this.currentTab = tabName
    }
  },

  components: { 
    appNav,
    appeals,
    assists
  },

  created() { 
  }
}
</script>

<style>
  .drop-shadow { 
    text-shadow: 1.5px 1.5px #000 !important;
  }
</style>
