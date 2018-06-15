<template>
  <div>
    <v-dialog v-model="dialogFlag" max-width="350">
      <v-card>
        <v-card-title class="headline grey--text text--darken-2">You are rating: {{helperName}}</v-card-title>
          <v-card-text class="text-xs-center">
            <emoji :rating="rating"/>
            <v-slider step="1" max="3" :color="colorThing" v-model="rating"></v-slider>
            <v-btn icon depressed color="grey lighten-2" @click="vote('dec')">
              <v-icon>fas fa-angle-left</v-icon>
            </v-btn>
            <v-btn icon depressed color="grey lighten-2" @click="vote('inc')">
              <v-icon>fas fa-angle-right</v-icon>
            </v-btn>
            <v-text-field 
              placeholder="Describe what you thought." 
              v-model="comment" 
              counter="255"
              rows="5"
              multi-line
            ></v-text-field>
            <v-btn 
              color="green darken-1" 
              depressed 
              block
              round 
              dark
              @click="rate"
            >Rate</v-btn>
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
    },

    redirectTo: { 
      default: null,
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
    dialogFlag: { 
      set(val) { 
        this.$emit('update:flag', val)
      },

      get() {
        return this.flag
      }
    },
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

      if(this.redirectTo != null) { 
        this.$router.push(this.redirectTo)
      }
    })

    .catch((res) => {
      console.log(res)
    })
  },
  }
}
</script>