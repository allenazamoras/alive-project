<template>
    <div>
        <v-navigation-drawer
            fixed
            :clipped="$vuetify.breakpoint.lgAndUp"
            app
            v-model="drawer"
            >
            <v-list dense>
            <template>
                <v-list-tile to="/">
                    <v-list-tile-action>
                        <v-icon>fas fa-home</v-icon>
                    </v-list-tile-action>
                    <v-list-tile-content>
                        <v-list-tile-title>
                        Home
                        </v-list-tile-title>
                    </v-list-tile-content>
                </v-list-tile>
                <v-list-tile to="/appeals">
                    <v-list-tile-action>
                        <v-icon>fas fa-list-alt</v-icon>
                    </v-list-tile-action>
                    <v-list-tile-content>
                        <v-list-tile-title>
                        Appeals
                        </v-list-tile-title>
                    </v-list-tile-content>
                </v-list-tile>
            </template>
            </v-list>
        </v-navigation-drawer>

        <v-toolbar
            color="indigo darken-1"
            dark
            dense
            flat
            app
            :clipped-left="$vuetify.breakpoint.mdAndUp"
            style="border-bottom: 1px solid #efefef !important;"
            fixed
            >
            <v-toolbar-title style="width: 300px" class="ml-0 pl-3">
                <v-toolbar-side-icon @click.stop="drawer = !drawer"></v-toolbar-side-icon>
                <span>ALIVE</span>
                <v-btn icon class="hidden-md-and-up">
                    <v-icon>search</v-icon>
                </v-btn>
            </v-toolbar-title>

            <v-text-field
                v-model="searchText"
                flat
                solo-inverted
                prepend-icon="search"
                label="Search"
                class="hidden-sm-and-down"
                @keyup.enter="search"
            >
            </v-text-field>

            <v-spacer></v-spacer>            
            <v-btn icon @click="createDialog = true">
                <v-icon>add</v-icon>
            </v-btn>
            <v-menu origin="top right" transition="scale-transition" bottom left offset-y max-height="250">
                <v-btn icon slot="activator">
                    <v-badge overlap>
                        <span slot="badge" class="caption" v-if="numOfNewNotifications > 0">{{ numOfNewNotifications }}</span>
                        <v-icon>notifications</v-icon>
                    </v-badge>               
                </v-btn>

                <v-list>
                    <div v-for="(item, index) in notifList" :key="`item-${index}`" :to="item.link" v-if="notifList.length > 0">
                        <v-list-tile @click="" :title="item.message">
                            <v-list-tile-title class="body-1"> <v-icon small>{{item.icon}} fa-fw</v-icon> {{item.message}}</v-list-tile-title>
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
                    <v-avatar size="32px">
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
        
        <create-appeal :createDialog.sync="createDialog" />
        <notifications :notifList.sync="notifList" />
    </div>
</template>

<script>
import createAppeal from './CreateAppeal'
import notifications from './Notifications'

import axios from "axios"
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
        searchText: ""
    }
  },

  methods: {
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
        "isLoggedIn", 
        "getUserData", 
        "getConfig"
    ])
  }
}
</script>