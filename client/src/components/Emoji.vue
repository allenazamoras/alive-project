<template>
  <div>
    <v-container>
      <v-layout>
        <v-flex>
          <div class="text-xs-center">
            <img width="125vw" :src="emojis[rating].img" alt="">
          </div>
          <br>
          <div class="text-xs-center">
            <span class="grey--text text--darken-2" style="font-style: italic;">{{emojis[rating].text}}</span>
          </div>
        </v-flex>
      </v-layout>
    </v-container>
  </div>
</template>

<script>
export default {
  data() {
    return { 
      emojis: [
        {
          img: require('../assets/rating/angry.svg'),
          text: "This didn't help at all!"
        },
        { 
          img: require('../assets/rating/confused.svg'),
          text: "This sucked. It wasn't what I expected."
        },
        { 
          img: require('../assets/rating/happy.svg'),
          text: "This helped me."
        },
        { 
          img: require('../assets/rating/grinning.svg'),
          text: "This is great!"
        }
      ]
    }
  },
  props: { 
    rating: { 
      type: Number,
      required: true
    }
  }
}
</script>
