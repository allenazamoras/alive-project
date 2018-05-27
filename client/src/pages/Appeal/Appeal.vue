<template>
  <div>
    <app-nav/>
    <v-container grid-list-lg>
      <v-layout justify-center>
        <v-flex lg7>
          <v-subheader>Categories</v-subheader>
          <v-layout row>
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
              <v-subheader>Most Recent Appeals</v-subheader>
            </v-flex>
            <v-layout row>
              <v-flex xs12 sm12 md9>
                <v-card class="elevation-3">
                  <v-list three-line>
                    <v-list-tile v-for="(appeal, index) in appeals" :key="`appeal-${index}`">
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
                          {{ appeal.owner.username }} <span class="grey--text text--lighten-1">{{ getMoment(appeal.date_pub) }}</span>
                        </v-list-tile-sub-title>
                      </v-list-tile-content>              
                      <v-list-tile-action>
                        <v-tooltip top>
                          <v-btn depressed slot="activator">
                            <h3><i class="fas fa-user-plus"></i></h3>
                          </v-btn>
                          <span>I can help!</span>
                        </v-tooltip>
                        
                      </v-list-tile-action>
                    </v-list-tile>
                  </v-list>
                </v-card>
              </v-flex>
              <v-flex xs4 sm4 md3>
                <v-card color="blue" class="white--text pa-3">
                  <v-card-media
                    src="src/assets/pills.svg"
                    height="100px"
                    contain
                  ></v-card-media>
                  <v-card-title primary-title>
                    <h3>kill me pls</h3>
                  </v-card-title>
                </v-card>
              </v-flex>
            </v-layout>
          </v-layout>
        </v-flex>
      </v-layout>   
    <v-dialog v-model="userDialog" max-width="500px">
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
    </v-dialog>
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

      appeals: []
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
