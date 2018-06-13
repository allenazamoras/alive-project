<template>
  <div>
    <v-card class="elevation-1">
      <v-card-text>
        <v-list>
          <v-list-tile>
            <v-list-tile-avatar>
              <img :src="`${api_url}${appeal.owner.profile_picture_url}`" :alt="appeal.owner.username">
            </v-list-tile-avatar>
            <v-list-tile-content>
              <v-list-tile-title>
                <router-link :to="`/profile/${appeal.owner.id}`" style="text-decoration: none;" class="subheading">
                  {{ appeal.owner.first_name + " " + appeal.owner.last_name}}
                </router-link>  
              </v-list-tile-title>
              <v-list-tile-sub-title>
                <router-link 
                  :to="`category/${appeal.category[0].id}`" 
                  style="text-decoration: none;"
                >
                  <span 
                    class="grey--text text--darken-1 caption"
                  >
                    Posted in {{ appeal.category[0].name }} around {{ getMoment(appeal.date_pub) }}
                  </span>
                </router-link>
              </v-list-tile-sub-title>
            </v-list-tile-content>
          </v-list-tile>
        </v-list>
        <v-card-text 
          v-if="!editMode"
        >
          <div class="headline">
            {{ appeal.request_title }}
          </div>
          <div class="body-1">
            {{ appeal.detail }}
            <div v-if="appeal.helper != null">
              <v-chip 
                disabled
                color="teal lighten-2" 
                text-color="white"
                class="mt-4 mb-0"
              >
                <v-avatar>
                  <v-icon>check_circle</v-icon>
                </v-avatar>
                <span>Helped by <span><router-link class="white--text" :to="`/profile/${appeal.helper.id}`"> {{appeal.helper.first_name + " " + appeal.helper.last_name }}</router-link></span></span>
              </v-chip>
            </div>
          </div>

          <div v-if="appeal.status != 'a' && appeal.rating.length > 0">
            <v-card-text class="ml-0 pl-0 grey--text text--darken-2">
              <v-avatar size="25">
                <img :src="emojis[appeal.rating[0].rating].img" alt="">
              </v-avatar>
              In the review, {{appeal.owner.first_name}} said: <span style="font-style: italic;">"{{appeal.rating[0].comment}}"</span>
            </v-card-text>
          </div>
          <v-card-text class="ml-0 pl-0 grey--text text--darken-2" v-else>
              <div v-if="appeal.owner.id != userID">
                {{appeal.owner.first_name}} hasn't rated the helper yet.
              </div>
              <div v-else>
                <v-btn depressed outline color="red accent-3" small round @click="ratingDialog = true">
                  Rate {{appeal.helper.first_name}}
                </v-btn>
              </div>
            </v-card-text>
        </v-card-text>

        <v-card-text v-else>
          <div class="headline">
            <v-text-field 
              class="headline"
              label="Title"
              placeholder="Describe it in a few words."
              v-model="request_title"
            >
            </v-text-field>
          </div>
          <div class="body-1">
            <v-text-field 
              label="Detail"
              placeholder="And expound it more here."
              v-model="detail"
            >
            </v-text-field>
          </div>

          <v-btn 
            depressed
            @click="save"
            round
            dark
            color="green darken-1"
          >
            <v-icon>save</v-icon>
            Save
          </v-btn>
          <v-btn 
            depressed
            dark
            color="red darken-2"
            @click="deletePrompt = true"
            round
          >
            <v-icon>delete</v-icon>
            Delete
          </v-btn>
          <v-btn 
            depressed
            color="grey lighten-2"
            @click="editMode = false"
            round
          >
            Cancel
          </v-btn>
        </v-card-text>
        <!-- <v-card-text>
          <v-btn round >
            Rate helper
          </v-btn>
        </v-card-text> -->
      </v-card-text>
      
      <v-btn
        style="z-index: 0;"
        small
        absolute
        dark
        fab
        top
        right
        color="pink"
        title="I want to help!"
        @click="bell"
        v-if="appeal.owner.id != userID && bellFlag == true"
      >
        <v-icon>notifications_active</v-icon>
      </v-btn>

      <v-fab-transition>
        <v-btn
          style="z-index: 0;"
          small
          dark
          fab
          absolute
          top
          right
          color="black"
          @click="setValues"
          v-if="appeal.owner.id == userID && !editMode && editFlag == true"
        >
          <v-icon>edit</v-icon>
        </v-btn>    
      </v-fab-transition>
      
    </v-card>

    <v-dialog v-model="deletePrompt" max-width="290" persistent>
      <v-card>
        <v-card-title class="headline grey--text text--darken-3">Are you sure you want to delete {{ appeal.request_title }}?</v-card-title>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn flat="flat" @click="deleteAppeal">Yes</v-btn>
          <v-btn flat="flat" @click="deletePrompt = false">No</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="requestDialog" max-width="290" persistent>
      <v-card>
        <v-card-title class="headline">Belling</v-card-title>
        <v-card-text>
          Waiting for requester to answer
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="red darken-1" flat="flat" @click="cancel">Cancel</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <rater v-if="ratingDialog" :flag.sync="ratingDialog" :appealID="appeal.id" :helperName="appeal.helper.first_name" :userID="appeal.helper.id"/>
  </div>
</template>

<script>
import Rater from './Rating'
import moment from 'moment'
import axios from 'axios'
import {mapGetters, mapState, mapMutations} from 'vuex'

export default {
  data() { 
    return {
      ratingDialog: false,
      pk: -1,
      editMode: false,
      api_url: process.env.API_URL,
      request_title: "",
      deletePrompt: false,
      detail: "",
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

  components: { 
    Rater
  },

  computed: { 
    requestDialog: { 
      set(val) { 
        this.setFlag(val)
      },
      get() { 
        return this.flag
      }
    },
    ...mapState('userModule', [
      'userID'
    ]),
    ...mapState('dialogModule', [
      'flag'
    ]),
    ...mapGetters('userModule', [
      'getConfig'
    ]),
  },

  methods: { 
    deleteAppeal() { 
      axios.delete(`${process.env.API_URL}/request/${this.appeal.id}/`, this.getConfig)
      .then((res) => { 
        this.deletePrompt = false
        this.editMode = false
      })

      .catch((res) => {
        console.log(res) 
      })
    },

    setValues() { 
      this.editMode = true
      this.request_title = this.appeal.request_title
      this.detail = this.appeal.detail
    },

    cancel() {
      this.setFlag(false)
      const url = `${process.env.API_URL}/pending/${this.pk}/`
      
      axios.delete(url, this.getConfig)
      .then((res) => { 
        this.snackbar = { 
          text: res.data.return,
          flag: true
        }
      })
    },

    save() { 
      axios.patch(`${process.env.API_URL}/request/${this.appeal.id}/`, {
          "request_title": this.request_title,
          "detail": this.detail
      }, this.getConfig)

      .then((res) => { 
          this.editMode = false
          console.log(res)
      })

      .catch((res) => { 
        console.log(res)
      })
    },

    getMoment(time) { 
      return moment(time, "YYYY-MM-DD hh:mm:ss").fromNow()
    },

    bell() { 
      console.log(this.appeal)
      this.setFlag(true)
      const url = `${process.env.API_URL}/pending/`

      axios.post(url, {
        "appeal.session_id": this.appeal.session_id
      }, this.getConfig)
      .then((res) => { 
        this.pk = res.data.id
        console.log(this.pk)  
      })
    },
    ...mapMutations('dialogModule', [
      'setFlag'
    ]),
  },

  props: { 
    appeal: {
      type: Object
    },
    bellFlag: { 
      default: true,
    },
    editFlag: { 
      default: true,
    }
  }
}
</script>