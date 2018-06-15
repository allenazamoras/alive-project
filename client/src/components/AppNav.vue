<template>
  <div>
    <!-- <v-navigation-drawer
      fixed
      :clipped="$vuetify.breakpoint.lgAndUp"
      app
      v-model="drawer"
    >
      <v-list dense>
      <template>
        <v-subheader>APPEALS</v-subheader>
        <v-list-tile to="/appeals/list">
          <v-list-tile-action>
            <v-icon>view_list</v-icon>
          </v-list-tile-action>
          <v-list-tile-content>
            <v-list-tile-title>
            View List
            </v-list-tile-title>
          </v-list-tile-content>
        </v-list-tile>
      </template>
      </v-list>
    </v-navigation-drawer> -->

    <v-toolbar
      color="indigo darken-1"
      dark
      dense
      flat
      app
      :clipped-left="$vuetify.breakpoint.mdAndUp"
      style="border-bottom: 1px solid #efefef !important;"
    >
      <v-toolbar-title style="width: 300px" class="ml-0 pl-3">
        <!-- <v-toolbar-side-icon @click.stop="drawer = !drawer"></v-toolbar-side-icon> -->
        <router-link to="/" style="text-transform: none; color: white; text-decoration: none;">
          <span>A<span style="font-weight: bold;">LIVE</span></span>
          <v-icon size="20" color="pink">fas fa-heartbeat</v-icon>
        </router-link>
      </v-toolbar-title>

      <!-- <v-text-field
        v-model="searchText"
        flat
        solo-inverted
        prepend-icon="search"
        label="Search"
        class="hidden-sm-and-down"
        @keyup.enter="search"
      >
      </v-text-field>        -->
      <v-spacer></v-spacer>
      <v-btn icon @click="createDialog = true">
        <v-icon size="20">add</v-icon>
      </v-btn>
      <v-menu 
        origin="top right" 
        transition="scale-transition" 
        content-class="notifContent"
        bottom 
        left 
        offset-y 
        max-height="350" 
        max-width="300"
      >
        <v-btn 
          icon 
          slot="activator"
          @click="markAsSeen"
        >
          <v-badge overlap>
            <span slot="badge" class="caption" v-if="numOfNewNotifications > 0">{{ numOfNewNotifications }}</span>
            <v-icon size="20">notifications</v-icon>
          </v-badge>               
        </v-btn>

          <v-list class="notifContent pl-1 pr-1 pa-2" three-line dense>
            <span class="body-1 pa-2 grey--text text--darken-2" @click=""><v-icon size="20">notifications</v-icon> Notifications</span>
            <v-divider></v-divider>
            <div 
              v-for="(item, index) in notifList" 
              :key="`item-${index}`" 
              v-if="notifList.length > 0" 
              :class="{'grey lighten-4': item.seen == false}" 
            >
              <v-list-tile :title="item.message">
                <v-list-tile-sub-title 
                    class="body-1"
                > 
                  <v-icon 
                    small
                  >
                    {{item.icon}} fa-fw
                  </v-icon> 
                    
                  <span class="black--text">
                    {{item.message}}
                  </span>
                  <v-icon size="15">access_time</v-icon> 
                  {{getMoment(item.date_created)}}
                </v-list-tile-sub-title>
              </v-list-tile>
              <v-divider v-if="index < notifList.length - 1"></v-divider>
            </div>
            
            <v-list-tile v-if="notifList.length == 0">
              <span class="grey--text body-1">
              No new notifications.
              </span>
            </v-list-tile>
          </v-list>
      </v-menu>
      <v-menu
        origin="top right"
        transition="scale-transition"
        :nudge-width="180"
        bottom
        right
        offset-y
      >
        <v-btn icon slot="activator">
          <span slot="badge" class="caption">3</span>
          <v-avatar size="25">
            <img :src="`${getUserData.profilePic}`">
          </v-avatar>             
        </v-btn>  
        <v-card>
          <v-list>
            <v-list-tile avatar>
                <v-list-tile-avatar>
                    <img :src="`${getUserData.profilePic}`" alt="John">
                </v-list-tile-avatar>
                <v-list-tile-content>
                    <v-list-tile-title>{{ getUserData.fullName }}</v-list-tile-title>
                    <v-list-tile-sub-title> @{{ getUserData.username }} </v-list-tile-sub-title>
                </v-list-tile-content>
            </v-list-tile>
          </v-list>
          <v-divider></v-divider>
          <v-list>
            <v-list-tile :to="`/profile/${getUserData.userID}`">
              <v-list-tile-action>
                <v-icon size="20">fas fa-user-circle</v-icon>
              </v-list-tile-action>
              <v-list-tile-title class="body-1">Profile</v-list-tile-title>
            </v-list-tile>
            <v-list-tile :to="`/settings`">
              <v-list-tile-action>
                <v-icon size="20">fas fa-cog</v-icon>
              </v-list-tile-action>
              <v-list-tile-title class="body-1">Settings</v-list-tile-title>
            </v-list-tile>
            <v-list-tile to="/logout">
              <v-list-tile-action>
                <v-icon size="20">fas fa-sign-out-alt</v-icon>
              </v-list-tile-action>
              <v-list-tile-title class="body-1">Logout</v-list-tile-title>
            </v-list-tile>
          </v-list>
        </v-card>
      </v-menu>  
    </v-toolbar>
    <v-text-field
      class="fade-transition"
      solo-inverted
      v-show="searchToggle"
    ></v-text-field>
    <!-- Opens the create appeal module -->
    <create-appeal :createDialog.sync="createDialog" />
    
    <!-- Polls notifs and is in charge of tracking requests -->
    <notifications :notifList.sync="notifList" />
  </div>
</template>

<script>
import createAppeal from './CreateAppeal'
import notifications from './Notifications'

import axios from "axios"
import moment from 'moment'
import { mapGetters, mapState, mapMutations } from "vuex"

export default {
  components: { 
    createAppeal,
    notifications
  },

  data() {
    return {
        createDialog: false,
        notifList: [],
        drawer: this.$vuetify.breakpoint.lgAndUp,
        searchText: "",
        searchToggle: false,

        test: false
    }
  },

  methods: {
    getMoment(time) { 
      return moment(time, "YYYY-MM-DD hh:mm:ss").fromNow()
    },

    markAsSeen() { 
        axios.post(`${process.env.API_URL}/notification/0/mark_seen/`, {
            seen: "True"
        }, this.getConfig)
        .then((res) => { 
            console.log(res)
        })
    },

    search() { 
        console.log(this.searchText)
        if(this.searchText.length > 0)
            this.$router.push(`/search/${this.searchText}`)
    }
  },

  computed: {
    numOfNewNotifications() {
      let ctr = 0

      for (let i = 0; i < this.notifList.length; i++) {
        if (!this.notifList[i].seen) {
          ctr++
        }
      }

      return ctr;
    },

    ...mapGetters("userModule", [
        "getUserData", 
        "getConfig"
    ])
  }
}
</script>