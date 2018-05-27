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

                        <h2 class="grey--text text--darken-4">{{ userInfo.fullName }}</h2>
                        <h3 class="body-1 grey--text text--darken-4"> {{ userInfo.bio }} </h3>
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
                        <span class="body-2">Username: </span> <router-link to="/">@{{ userInfo.username }}</router-link>
                      </span>
                      <br>
                      <span>
                        <span class="body-2">Full Name: </span> {{ userInfo.fullName }}
                      </span>
                      <br>
                      <span>
                        <span class="body-2">Gender: </span> {{ userInfo.gender }}
                      </span>
                      <br>
                      <span>
                        <span class="body-2">Joined Date: </span> {{ userInfo.joinedDate }}
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
                <v-tabs icons-and-text class="elevation-1">
                  <v-tabs-slider color="black"></v-tabs-slider>
                  <v-tab href="#tab-appeals">
                    <v-icon>fas fa-hands</v-icon>
                    Appeals ({{ userInfo.appeals.length }})
                  </v-tab>
                  <v-tab href="#tab-assists">
                    <v-icon>fas fa-handshake</v-icon>
                    Assists ({{ userInfo.assists.length }})
                  </v-tab>
                  <v-tab-item
                    v-for="tab in tabs"
                    :key="tab"
                    :id="'tab-' + tab"
                  >
                    <v-card flat>
                      <appeals :appeals="userInfo.appeals" v-show="tab == 'appeals'"></appeals>
                      <appeals :appeals="userInfo.assists" v-show="tab == 'assists'"></appeals>
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

export default {
  data() { 
    return {
      userInfo: {
        username: "johndoe",
        fullName: "John Doe",
        gender: "Male",
        bio: "Programmer | Knee Gore | I want 2 live oh wow",
        joinedDate: "May 27, 2018",
        appeals: [
          {
            title: "I want to eat my dog because he keeps hitting me",
            detail: "Is it better if I marinate it overnight or for an hour?",
            datePosted: "May 27, 2018",
            status: "active"
          },

          {
            title: "I want to eat my cat because he keeps hitting me",
            detail: "Is it better if I marinate it overnight or for an hour?",
            datePosted: "May 27, 2018",
            status: "completed"
          },

          {
            title: "I want to eat my pig because he keeps hitting me",
            detail: "Is it better if I marinate it overnight or for an hour?",
            datePosted: "May 27, 2018",
            status: "completed"

          },
        ],

        assists: [
          {
            title: "I want to eat my dog because he keeps hitting me",
            detail: "Is it better if I marinate it overnight or for an hour?",
            datePosted: "May 27, 2018",
            status: "active"
          },

          {
            title: "I want to eat my dog because he keeps hitting me",
            detail: "Is it better if I marinate it overnight or for an hour?",
            datePosted: "May 27, 2018",
            status: "active"
          },

          {
            title: "I want to eat my dog because he keeps hitting me",
            detail: "Is it better if I marinate it overnight or for an hour?",
            datePosted: "May 27, 2018",
            status: "completed"
          },

          {
            title: "I want to eat my dog because he keeps hitting me",
            detail: "Is it better if I marinate it overnight or for an hour?",
            datePosted: "May 27, 2018",
            status: "completed"
          },
        ],
      },

      viewedUsername: this.$route.params.username,
      patternURL: require('../../assets/sun-pattern.png'),
      tabs: ["appeals", "assists"],


      //For the Awards
      firstReviewReceived: require("../../assets/achievements/medal.svg"),
      firstAssist: require("../../assets/achievements/badge.svg")
    }
  },

  components: { 
    appNav,
    appeals
  },

  created() {
    
  }
}
</script>