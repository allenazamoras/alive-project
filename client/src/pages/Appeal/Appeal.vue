<template>
  <v-container grid-list-lg>
    <v-subheader>Categories</v-subheader>
    <v-layout row>
      <v-flex xs8 md2 v-for="(category, index) in categories" :key="`category-${index}`">
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
    <v-card>
      <v-list two-line>
        <template v-for="(item, index) in recentAppeals">
          <v-subheader v-if="item.header" :key="item.header">{{ item.header }}</v-subheader>
          <v-divider v-else-if="item.divider" :inset="item.inset" :key="index"></v-divider>
          <v-list-tile v-else :key="item.title" avatar>
            <v-list-tile-avatar>
              <img :src="item.avatar">
            </v-list-tile-avatar>
            <v-list-tile-content>
              <v-list-tile-title v-html="item.title"></v-list-tile-title>
              <v-list-tile-sub-title v-html="item.subtitle"></v-list-tile-sub-title>
            </v-list-tile-content>
          </v-list-tile>
        </template>
      </v-list>
    </v-card>
    
    
  </v-container>
</template>

<script>
export default {
  data() { 
    return { 
      categories: [
        {name: "School", url: "/appeal/category/school", img: "https://picsum.photos/200/300/?random"},
        {name: "Work", url: "/appeal/category/work", img: "https://picsum.photos/200/300/?random"},
        {name: "Family", url: "/appeal/category/family", img: "https://picsum.photos/200/300/?random"},
        {name: "Others", url: "/appeal/category/others", img: "https://picsum.photos/200/300/?random"},
      ],
      recentAppeals: [
        { avatar: 'https://vuetifyjs.com/static/doc-images/lists/1.jpg', title: 'Bob needs help in School', subtitle: "<span class='text--primary'>Ali Connors</span> &mdash; I'll be in your neighborhood doing errands this weekend. Do you want to hang out?" },
        { divider: true, inset: true },
        { avatar: 'https://vuetifyjs.com/static/doc-images/lists/2.jpg', title: 'Summer BBQ <span class="grey--text text--lighten-1">4</span>', subtitle: "<span class='text--primary'>to Alex, Scott, Jennifer</span> &mdash; Wish I could come, but I'm out of town this weekend." },
        { divider: true, inset: true },
        { avatar: 'https://vuetifyjs.com/static/doc-images/lists/3.jpg', title: 'Oui oui', subtitle: "<span class='text--primary'>Sandra Adams</span> &mdash; Do you have Paris recommendations? Have you ever been?" }
      ],
    }
  },


}
</script>
