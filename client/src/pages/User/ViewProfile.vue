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
            src="https://vuetifyjs.com/static/doc-images/parallax/material2.jpg"
          >
            <v-container pa-0 fill-height>
              <v-layout justify-center align-end wrap>
                <v-flex text-xs-center xs12>
                  <v-avatar size="60">
                    <img :src="api_url + user.profile_picture_url" alt="">
                  </v-avatar>
                  <h3 class="headline white--text">{{ user.first_name + " " + user.last_name }}</h3>
                  <h1 class="subheading white--text">@{{user.username}}</h1>
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
                    <v-tab @click="changeTab('rep_received')">
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
    }
  },

  components: { 
    appeals,
    appealView
  },

  methods: { 
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