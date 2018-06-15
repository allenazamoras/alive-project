<template>
  <div>
    <v-container pb-0>
      <v-layout
        row
        wrap
        justify-center
      >
        <v-flex xs12 sm10 md10 lg8>
          <v-jumbotron
            class="pa-0 elevation-2"
            height="300px"
            color="indigo"
          >
            <v-container pa-0 fill-height>
              <v-layout justify-center align-end wrap>
                <v-flex text-xs-center xs12>
                  <v-avatar size="60">
                    <img :src="api_url + user.profile_picture_url" alt="">
                  </v-avatar>
                  <h3 class="headline white--text">{{ user.first_name + " " + user.last_name }}</h3>
                  <h1 class="subheading white--text grey--text text--lighten-2" style="font-style: italic;">@{{user.username}}</h1>
                  <h1 class="subheading white--text">{{user.gender}}</h1>
                </v-flex>
                <v-flex
                  text-xs-center
                  xs12
                >
                  <v-tabs 
                    class="elevation-3"
                    centered
                  >
                    <v-tab @click="changeTab('appeals')">
                      Appeals
                    </v-tab>
                    <v-tab @click="changeTab('assists')">
                      Assists
                    </v-tab>
                    <v-tab @click="changeTab('ratings_received')">
                      Ratings Received
                    </v-tab>
                  </v-tabs>
                </v-flex>
              </v-layout>
            </v-container>
          </v-jumbotron>
        </v-flex>
      </v-layout>
    </v-container>
    <div v-show="currentTab == 'appeals'">
      <v-container
        pt-0
        grid-list-xl
        fill-height
        >
        <v-layout
          row
          wrap
          justify-center
        >
          <v-flex xs12 sm10 md10 lg8>
            <v-subheader class="pl-0">Active</v-subheader>
            <appeal-view v-if="user.openappeals.length > 0" :appeal="user.openappeals[0]"/>
          </v-flex>
          <v-flex xs12 text-xs-center v-if="user.openappeals.length == 0">
            <span class="grey--text text--darken-2">{{user.first_name}} doesn't seem to have any active appeals.</span>
          </v-flex>
        </v-layout>
      </v-container>
      <v-container
        pt-0
        grid-list-xl
        fill-height
        >
        <v-layout
          row
          justify-center
        >
          <v-flex xs12 sm10 md10 lg8 >
            <v-subheader class="pl-0">Completed</v-subheader>
            <v-layout
              row
              justify-center
              wrap
            >
              <v-flex xs12 v-if="user.closedappeals.length > 0" v-for="appeal in user.closedappeals" :key="appeal.id">
                <appeal-view :appeal="appeal" :bellFlag="`false`" :editFlag="`false`"/>
              </v-flex>
              <v-flex xs12 v-if="user.closedappeals.length == 0" text-xs-center>
                <span class="grey--text text--darken-2">{{user.first_name}} doesn't seem to have any completed appeals.</span>
              </v-flex>
            </v-layout>
          </v-flex>
        </v-layout>
      </v-container>
    </div>
    <div v-show="currentTab == 'assists'">
      <v-container
        pt-0
        grid-list-xl
        fill-height
        >
        <v-layout
          row
          justify-center
        >
          <v-flex xs12 sm10 md10 lg8 >
            <v-subheader class="pl-0">Assists</v-subheader>
            <v-layout
              row
              justify-center
              wrap
            >
              <v-flex xs12 v-if="user.offers.openappeals.length > 0" v-for="appeal in user.offers.openappeals" :key="appeal.id">
                <appeal-view :appeal="appeal" :bellFlag="`false`" :editFlag="`false`"/>
              </v-flex>
              <v-flex xs12 v-if="user.offers.openappeals.length == 0" text-xs-center>
                <span class="grey--text text--darken-2">{{user.first_name}} doesn't seem to have any assists.</span>
              </v-flex>
            </v-layout>
          </v-flex>
        </v-layout>
      </v-container>
    </div>
    <div v-show="currentTab == 'ratings_received'">
      <v-container
        pt-0
        grid-list-xl
        fill-height
        >
        <v-layout
          row
          justify-center
        >
          <v-flex xs12 sm10 md10 lg8 >
            <v-subheader class="pl-0">Rating</v-subheader>
            <v-layout
              row
              justify-center
              wrap
            >
              <v-flex xs12 sm8 md6 lg5>
                <v-card class="pa-2">
                  <v-card-text>
                    <span class="headline grey--text text--darken-3">Overall Rating</span>
                  </v-card-text>
                  <v-card-text>
                      <v-layout row wrap v-for="(rating, index) in user.overallrating" align-center :key="`rating-${index}`">
                          <v-flex xs2 sm2 md1 lg1 xl1>
                            <v-avatar size="25" class="pr-2">
                              <img :src="emojis[index].img" alt="">
                            </v-avatar>
                          </v-flex>
                          <v-flex>
                            <v-progress-linear
                              class="ma-0" 
                              :value="percentVal(rating)" 
                              :color="getColor(index, rating)"
                              height="10"
                              ></v-progress-linear>
                              <span 
                                class="grey--text text--darken-2 caption"
                                style="font-style: italic;"
                              >
                                <span v-if="rating == 0">
                                  No votes
                                </span>
                                <span v-else>
                                {{rating}}
                                  <span v-if="rating > 1">users</span>
                                  <span v-else>user</span>
                                  voted this
                                </span>
                              </span>
                          </v-flex>
                      </v-layout>
                  </v-card-text>
                </v-card>
              </v-flex>
              <!-- <v-flex xs12 sm12 md6 lg7>
                <div v-if="ratings.length == 0">
                  <span class="grey--text text--darken-1">{{user.first_name}} hasn't received any ratings yet.</span>
                </div>
                <div v-for="rating in ratings" v-if="ratings.length > 0">
                  {{rating}}
                </div>
              </v-flex> -->
            </v-layout>
          </v-flex>
        </v-layout>
      </v-container>
    </div>
  </div>
</template>

<script>
//Components
import appeals from '../.././components/User/Appeals'
import appealView from '../../components/AppealView'

//Plugins
import axios from 'axios'
import {mapGetters} from 'vuex'

export default {
  data() { 
    return {
      api_url: process.env.API_URL,
      currentTab: "appeals",
      cycle: false,

      emojis: [
        {
          img: require('../../assets/rating/angry.svg'),
          text: "This didn't help at all!"
        },
        { 
          img: require('../../assets/rating/confused.svg'),
          text: "This sucked. It wasn't what I expected."
        },
        { 
          img: require('../../assets/rating/happy.svg'),
          text: "This helped me."
        },
        { 
          img: require('../../assets/rating/grinning.svg'),
          text: "This is great!"
        }
      ],

      //user info 
      user: {
        openappeals: [],
        closedappeals: [],
        offers: { 
          openappeals: [],
          closedappeals: []
        }
      },
      viewedUsername: this.$route.params.username,
      owner: {},
      ratings: [],
    }
  },

  components: { 
    appeals,
    appealView
  },

  methods: { 
    getColor(index, numOfPeople) { 
      let color = ""

      if(numOfPeople == 0) { 
        color = "grey lighten-2"
      } else if(numOfPeople > 0) { 
        switch(index) { 
          case '0': color = "red"
                  break
          case '1': color = "orange"
                  break
          case '2': color = "cyan"
                  break
          case '3': color = "indigo"
                  break
        }        
      }

      return color
    },
    percentVal(numOfPeople) { 
      return (numOfPeople / this.totalPeopleRating) * 100
    },

    changeTab(tab) { 
      this.currentTab = tab
    },

    getProfileData() { 
      axios.get(`${process.env.API_URL}/user/${this.$route.params.username}/`, this.getConfig)
      .then((res) => { 
        this.user = res.data
      })
      .catch((err) => { 
        console.log(err)
      })

      axios.get(`${process.env.API_URL}/rating/`, this.getConfig)
      .then((res) => { 
        this.ratings = res.data['ratings_received']
      })
    }
  },

  computed: { 
    totalPeopleRating() { 
      let total = 0

      for(let i = 0; i < 4; i++) { 
        total += this.user.overallrating[`${i}`]
      }

      return total
    },
    ...mapGetters('userModule', [
      'getConfig'
    ])
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