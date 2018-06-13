<template>
  <div>
    <v-dialog v-model="flag" max-width="350" persistent>
      <v-card>
        <v-card-title class="headline">You are rating: {{helperName}}</v-card-title>
          <v-card-text class="text-xs-center">
            <emoji :rating="rating"/>
            <v-slider step="1" max="3" :color="colorThing" v-model="rating"></v-slider>
            <v-btn icon depressed @click="vote('dec')">
              <v-icon>fas fa-angle-left</v-icon>
            </v-btn>
            <v-btn icon depressed @click="vote('inc')">
              <v-icon>fas fa-angle-right</v-icon>
            </v-btn>
            <v-text-field placeholder="Describe what you thought." v-model="comment" multi-line counter="255"></v-text-field>
            <v-btn color="green darken-1" depressed round dark block @click="rate">Rate</v-btn>
          </v-card-text>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import Emoji from './Emoji'

import {mapGetters} from 'vuex'
import axios from 'axios'
export default {
  data() { 
    return { 
      rating: 2,
      comment: "",
      colorThing: "cyan"
    }
  },
  props: { 
    flag: { 
      type: Boolean,
      default: false
    },
    appealID: {
      required: true
    },
    helperName: { 
      required: true
    },
    userID: { 
      required: true
    }
  },

  components: { 
    Emoji
  },

  watch: { 
    rating: function(val, oldVal) { 
      switch(val) { 
        case 0: this.colorThing = "red"
                break
        case 1: this.colorThing = "orange"
                break
        case 2: this.colorThing = "cyan"
                break
        case 3: this.colorThing = "indigo"
                break
      }
    },
  },

  computed: { 
    ...mapGetters('userModule', [
      'getConfig'
    ])
  },

  methods: { 
    vote(action) { 
      switch(action) { 
        case 'dec': if(this.rating > 0) this.rating--
                    break
        case 'inc': if(this.rating < 3) this.rating++
                    break
      }
    },
    rate() { 
    axios.post(`${process.env.API_URL}/rating/`, {
      "user": parseInt(this.userID),
      "appeal": parseInt(this.appealID),
      "rating": parseInt(this.rating),
      "comment": this.comment
    }, this.getConfig)

    .then((res) => { 
      this.$emit('update:flag', false)
      console.log(res)
    })

    .catch((res) => {
      console.log(res)
    })
  },
  }
}
</script>