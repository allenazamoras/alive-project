<template>
  <div>
    <v-card class="elevation-1">
      <v-card-text>
        <v-list>
          <v-list-tile>
            <v-list-tile-avatar>
              <img :src="appeal.owner.profile_picture" :alt="appeal.owner.username">
            </v-list-tile-avatar>
            <v-list-tile-content>
              <v-list-tile-title >
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
            <div v-if="appeal.helper">
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
  </div>
</template>

<script>
import moment from 'moment'
import axios from 'axios'
import {mapGetters, mapState, mapMutations} from 'vuex'

export default {
  data() { 
    return { 
      pk: -1,
      editMode: false,

      request_title: "",
      deletePrompt: false,
      detail: "",
    }
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
      default: []
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