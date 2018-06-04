<template>
  <div>
    <app-nav/>
    <v-container grid-list-lg>
      <v-layout justify-center row>
          <v-flex>
          <v-layout wrap justify-center>
            <v-flex xs12>
              <v-subheader class="pl-0">Most Recent Appeals</v-subheader>
            </v-flex>
            <v-layout row>
              <v-flex xs12 sm12 md12>
                <v-card class="elevation-3">
                  <v-list three-line>
                    <div v-for="(appeal, index) in appeals" :key="`appeal-${index}`">
                      {{ appeal }}
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
                          <v-btn depressed slot="activator" @click="bell(appeal.session_id)">
                            <h3><v-icon>notifications</v-icon> Bell</h3>
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


    <v-dialog v-model="userDialog" max-width="290" persistent>
      <v-card>
        <v-card-title class="headline">Belling</v-card-title>
        <v-card-text>
          Waiting for requester to answert
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="green darken-1" flat="flat" @click.native="userDialog = false">Cancel</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
  
</template>

<script>
import appNav from '../.././components/AppNav.vue'

import moment from 'moment'
import axios from 'axios'
import {mapGetters, mapMutations} from 'vuex'

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

  computed: { 
    ...mapGetters('userModule', [
      'getConfig'
    ])
  },

  methods: {
    getMoment(time) { 
      console.log(time)
      return moment(time, "YYYY-MM-DD hh:mm:ss").fromNow()
    },

    bell(session_id) { 
      this.userDialog = true
      console.log(session_id)
      axios.post(`${process.env.API_URL}/pending/`, {
        "appeal.session_id": session_id
      }, this.getConfig)
      .then((res) => { 
        console.log(res)
      })
    },

    ...mapMutations('sessionModule', [
      'setSession'
    ])
  },

  created() { 
    axios.get(`${process.env.API_URL}/request/`, this.getConfig)
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

