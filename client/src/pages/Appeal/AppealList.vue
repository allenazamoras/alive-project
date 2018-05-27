<template>
  <div>
    <app-nav/>
    <v-container grid-list-lg>
      <v-layout justify-center row>
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
          </v-layout> 
          
          <v-layout wrap justify-center>
            <v-flex xs12>
              <v-subheader class="pl-0">Most Recent Appeals</v-subheader>
            </v-flex>
            <v-layout row>
              <v-flex xs12 sm12 md12>
                <v-card class="elevation-3">
                  <v-list three-line>
                    <div v-for="(appeal, index) in appeals" :key="`appeal-${index}`">
                      <v-list-tile>
                        <v-list-tile-avatar>
                          <img src="https://picsum.photos/200/300/?random" :alt="appeal.owner.username">
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
                          <v-btn depressed slot="activator">
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

      <!-- dialog component -->
    <!-- <v-dialog v-model="userDialog" max-width="500px">
      <v-card>
        <v-card-title>
          <span>Dialog 3</span>
          <v-spacer></v-spacer>
          <v-menu bottom left>
            <v-btn slot="activator" icon>
              <v-icon>more_vert</v-icon>
            </v-btn>
          
          </v-menu>
        </v-card-title>
        <v-card-actions>
          <v-btn color="primary" flat @click.stop="userDialog = false">Close</v-btn>
        </v-card-actions>
      </v-card>    
    </v-dialog> -->
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
        {name: "Dahyun Best Girl", url: "/appeal/category/family", img: "https://picsum.photos/200/300/?random"},
        {name: "Others", url: "/appeal/category/others", img: "https://picsum.photos/200/300/?random"},
      ],

      appeals: [
        {
          owner: { 
            username: "johndoe"
          },

          request_title: "I want to cook my dog",
          detail: "But then I don't have the sauce for it",
          date_pub: "20180527"
        },

        {
          owner: { 
            username: "johndee"
          },

          request_title: "I want to cook my cat",
          detail: "But then I don't have the sauce for it",
          date_pub: "20180526"
        }
      ]
    }
  },

  methods: {
    getMoment(time) { 
      return moment(time, "YYYY-MM-DD").fromNow()
    }
  },

  created() { 
    axios.get("http://192.168.1.2:8000/request/")
    .then((res) => { 
      this.appeals = res.data
    })
  },

  components: { 
    appNav
  }
}
</script>

<style>
  .drop-shadow { 
    text-shadow: 1.5px 1.5px #000;
  }
</style>

