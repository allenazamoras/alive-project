<template>
  <v-container grid-list-lg>
    <v-subheader>Categories</v-subheader>
    <v-layout row wrap pl-3>
      <v-flex xs4 sm3 md2 v-for="(category, index) in categories" :key="`category-${index}`">
        <v-card 
          :to="category.url">
          <v-card-media 
            :src="category.img"
            height="125px">

          </v-card-media>
          <v-card-title primary-title>
            {{ category.name }}
          </v-card-title>
        </v-card>
      </v-flex>
    </v-layout>    

    <v-subheader>Most Recent Appeals</v-subheader>
    <v-layout row pl-3>
      <v-flex xs8 md8>
        <v-card>
          <v-list three-line>
            <v-list-tile v-for="(appeal, index) in recentAppeals" :key="`appeal-${index}`">
              <v-list-tile-avatar>
                <img :src="appeal.photoURL" :alt="appeal.username">
              </v-list-tile-avatar>
              <v-list-tile-content :to="appeal.url">
                <v-list-tile-title>
                  {{ appeal.detail}}
                </v-list-tile-title>
                <v-list-tile-sub-title>
                  <span class="text--primary">
                    {{ appeal.username }}
                  </span>
                  <router-link :to="appeal.url" class="grey--text text--lighten-1">{{ getMoment(appeal.time) }}</router-link>
                </v-list-tile-sub-title>
              </v-list-tile-content>              
              <v-list-tile-action>
                <v-btn flat color="success">
                  HELP
                </v-btn>
              </v-list-tile-action>
            </v-list-tile>
          </v-list>
        </v-card>
      </v-flex>
      <v-flex xs4 md4>
        <v-card color="purple" class="white--text">
          <v-container fluid grid-list-lg>
            <v-layout row>
              <v-flex xs7>
                <div>
                  <div class="headline">all lives matter</div>
                  <div>KNEE GORES</div>
                </div>
              </v-flex>
              <v-flex xs5>
                <v-card-media
                  src="https://i.redditmedia.com/qqdn-TPzvqf3PrpUgzAM9Ls8zM3-jkbVg239HKQkmeg.jpg?fit=crop&crop=faces%2Centropy&arh=2&w=640&s=6aac4b496bd3d084b21cd44cd23f7c24"
                  height="125px"
                  contain
                ></v-card-media>
              </v-flex>
            </v-layout>
          </v-container>
        </v-card>
      </v-flex>
     
    </v-layout>
    
  </v-container>
</template>

<script>
import moment from 'moment'

export default {
  data() { 
    return { 
      categories: [
        {name: "School", url: "/appeal/category/school", img: "https://picsum.photos/200/300/?random"},
        {name: "Work", url: "/appeal/category/work", img: "https://picsum.photos/200/300/?random"},
        {name: "Family", url: "/appeal/category/family", img: "https://picsum.photos/200/300/?random"},
        {name: "Others", url: "/appeal/category/others", img: "https://picsum.photos/200/300/?random"},
        {name: "School", url: "/appeal/category/school", img: "https://picsum.photos/200/300/?random"},
        {name: "Work", url: "/appeal/category/work", img: "https://picsum.photos/200/300/?random"},
        {name: "Family", url: "/appeal/category/family", img: "https://picsum.photos/200/300/?random"},
        {name: "Others", url: "/appeal/category/others", img: "https://picsum.photos/200/300/?random"},
      ],
      recentAppeals: [
        {url: "/appeal/4/", photoURL: "https://vuetifyjs.com/static/doc-images/lists/1.jpg", username: "bob", detail: "I need help with mah studiez cause I wanna die lol", category: "school", categoryURL: "/appeal/category/school", time: "20180525"},
        {url: "/appeal/3/", photoURL: "https://vuetifyjs.com/static/doc-images/lists/1.jpg", username: "bob", detail: "I can't open this jar", category: "school", categoryURL: "/appeal/category/school", time: "20101031"},
        {url: "/appeal/2/", photoURL: "https://vuetifyjs.com/static/doc-images/lists/1.jpg",  username: "bob", detail: "What is Love I wanna know oh i wanna know", category: "school", categoryURL: "/appeal/category/school", time: "20090930"},
        {url: "/appeal/1/", photoURL: "https://vuetifyjs.com/static/doc-images/lists/1.jpg",  username: "bob", detail: "Dahyun best girl", category: "school", categoryURL: "/appeal/category/school", time: "20080825"},
      ],
    }
  },

  methods: {
    getMoment(time) { 
      return moment(time, "YYYYMMDD").fromNow()
    }
  }
}
</script>
