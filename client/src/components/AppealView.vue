<template>
  <div>
    <v-card class="elevation-1">
      <v-card-text class="pa-0">
        <v-list>
          <v-list-tile>
            <v-list-tile-avatar size="30">
              <img :src="`${api_url}${appeal.owner.profile_picture_url}`" :alt="appeal.owner.username">
            </v-list-tile-avatar>
            <v-list-tile-content>
              <v-list-tile-title>
                <router-link 
                  :to="`/profile/${appeal.owner.id}`" 
                  style="text-decoration: none;" 
                  class="body-1 grey--text text--darken-3"
                >
                  {{ appeal.owner.first_name + " " + appeal.owner.last_name}}
                </router-link>  
              </v-list-tile-title>
              <v-list-tile-sub-title>
                <router-link 
                  :to="`/category/${appeal.category[0].id}`" 
                  style="text-decoration: none;"
                >
                  <span 
                    class="caption grey--text text--darken-1 caption"
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
          class="pa-0"
        >
          <v-card-text>
            <div class="headline grey--text text--darken-3" style="font-family: 'Crimson Text', serif;">
              <blockquote>{{ appeal.request_title }}</blockquote>
            </div>
            <div class="subheading pa-4 grey--text text--darken-2" style="text-align: justify;">
              {{ appeal.detail }}
            </div>
          </v-card-text>
          <v-divider v-if="appeal.helper != null" class="mt-2 mb-2"></v-divider>
          <v-card-text class="pl-0 pr-3 pt-1 pb-1" v-if="appeal.helper != null">
            <v-chip 
              disabled
              small
              text-color="white"
              color="teal lighten-2" 
              class="mt-1 mb-0 ml-3"
            >
              <v-avatar>
                <v-icon>check_circle</v-icon>
              </v-avatar>
              <span>Helped by <span><router-link class="white--text" :to="`/profile/${appeal.helper.id}`"> {{appeal.helper.first_name + " " + appeal.helper.last_name }}</router-link></span></span>
            </v-chip>
          </v-card-text>
          <div v-if="appeal.status != 'a' && appeal.rating.length > 0" class="pl-3 pr-3">
            <v-card-text class="ml-0 pt-2 pb-3 pl-0 grey--text text--darken-2">
              <v-avatar size="25">
                <img :src="emojis[appeal.rating[0].rating].img" alt="">
              </v-avatar> 
              {{appeal.owner.first_name}} rated {{appeal.helper.first_name}} with
              <span style="font-style: italic;">"{{appeal.rating[0].comment}}"</span>
            </v-card-text>
          </div>
          <v-card-text class="ml-0 pl-0 pt-0 pb-3 grey--text text--darken-2" v-if="appeal.status != 'a' && appeal.rating.length == 0">
              <div v-if="appeal.owner.id != userID" class="pl-3 pr-3">
                <span style="font-style: italic;">
                  <span v-if="appeal.owner.id != userID"></span>
                  {{appeal.owner.first_name}} 
                </span>
              </div>
              <div class="pl-2 pr-3" v-if="appeal.helper != null">
                <v-btn depressed color="yellow darken-4" dark small @click="ratingDialog = true">
                  <v-icon size="12">fas fa-star fa-fw</v-icon>
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

<style>
  blockquote {
    font-family: Georgia, serif;
    font-style: italic;
    width: 500px;
    margin: 0.25em 0;
    padding: 0.35em 40px;
    line-height: 1.45;
    position: relative;
  }

  blockquote:before {
    display: block;
    padding-left: 10px;
    content: "\201C";
    font-size: 80px;
    position: absolute;
    left: -20px;
    top: -20px;
    color: #b1b1b1;
  }
</style>
