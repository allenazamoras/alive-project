<template>
  <div>
    <app-nav></app-nav>
    <v-container pb-0>
      <div class="elevation-5">

      </div>
      <v-layout
        row
        wrap
        justify-center
      >
        <v-flex xs12 sm10 md10 lg8>
          <v-jumbotron
            class="pa-0"
            height="300px"
            :gradient="gradient"
            src="https://vuetifyjs.com/static/doc-images/parallax/material2.jpg"
          >
            <v-container fill-height>
              <v-layout justify-center align-end wrap>
                <v-flex text-xs-center xs12>
                  <v-avatar size="60">
                    <img :src="user.profile_picture" alt="">
                  </v-avatar>
                  <h3 class="headline white--text">{{ user.first_name + " " + user.last_name }}</h3>
                </v-flex>
                <v-flex
                  text-xs-center
                  xs12
                >
                  <v-tabs class="elevation-3">
                    <v-tab @click="changeTab('assists')">
                      Appeals
                    </v-tab>
                    <v-tab @click="changeTab('assists')">
                      Assists
                    </v-tab>
                    <v-tab @click="changeTab('assists')">
                      Ratings Given
                    </v-tab>
                    <v-tab @click="changeTab('assists')">
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
    <v-container
      pt-0
      grid-list-xl
      fill-height
      >
      <v-layout
        row
        justify-center
      >
        <v-flex xs12 sm10 md10 lg8>
          <v-subheader class="pl-0">Active</v-subheader>
          <appeal-view :appeal="user.openappeals[0]"/>
          {{user.openappeals}}
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
        <v-flex xs12 sm10 md10 lg8>
          <v-subheader class="pl-0">Completed</v-subheader>
          {{user.closedappeals}}
        </v-flex>
      </v-layout>
    </v-container>
  </div>
</template>

<script>
//Components
import appNav from '../.././components/AppNav'
import appeals from '../.././components/User/Appeals'
import appealView from '../../components/AppealView'

//Plugins
import axios from 'axios'
import {mapGetters} from 'vuex'

export default {
  data() { 
    return {
      patternURL: require('../../assets/sun-pattern.png'),
      currentTab: "appeals",
      cycle: false,

      //user info 
      user: {},
      viewedUsername: this.$route.params.username,

      gradient: 'to top right, rgba(63,81,181, .7), rgba(25,32,72, .7)',

      //awards
      firstReviewReceived: require("../../assets/achievements/medal.svg"),
      firstAssist: require("../../assets/achievements/badge.svg"),
    }
  },

  components: { 
    appNav,
    appeals,
    appealView
  },

  methods: { 
    changeTab() { 
      console.log("HI")
    },

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