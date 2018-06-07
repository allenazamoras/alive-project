<template>
  <div>
    <v-card class="elevation-2">
      <v-card-text>
        <v-list>
          <v-list-tile>
            <v-list-tile-avatar>
              <img :src="appeal.owner.profile_picture" :alt="appeal.owner.username">
            </v-list-tile-avatar>
            <v-list-tile-content>
              <v-list-tile-title>
                <router-link :to="`/profile/${appeal.owner.id}`" style="text-decoration: none;" class="subheading">
                  {{ appeal.owner.first_name + " " + appeal.owner.last_name}}
                </router-link>
              </v-list-tile-title>
              <v-list-tile-sub-title>
                <router-link to="" style="text-decoration: none;">
                  <span class="grey--text text--darken-1 caption">Posted {{ getMoment(appeal.date_pub) }}</span>
                </router-link>
              </v-list-tile-sub-title>
            </v-list-tile-content>
          </v-list-tile>
        </v-list>
        <v-card-text class="">
          <div class="display-1">
            {{ appeal.request_title }}
          </div>
          <div class="body-1">
            {{ appeal.detail }}
          </div>
        </v-card-text>
        <v-chip v-for="i in 5" outline color="grey" disabled small>
            Family
        </v-chip>
      </v-card-text>
      <v-card-actions>

      </v-card-actions>

      <v-btn
        small
        absolute
        dark
        fab
        top
        right
        color="pink"
        title="I want to help!"
        @click="bell({session_id: appeal.session_id})"
        v-if="appeal.owner.id != userID"
      >
        <v-icon>notifications_active</v-icon>
      </v-btn>

      <v-btn
        small
        absolute
        dark
        fab
        top
        right
        color="black"
        title="I want to help!"
        @click="edit"
        v-else
      >
        <v-icon>edit</v-icon>
      </v-btn>
    </v-card>


    <v-dialog v-model="promptDialog" max-width="290" persistent>
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
    }
  },

  computed: { 
    ...mapGetters('userModule', [
      'getConfig'
    ]),

    ...mapState('userModule', [
      'userID'
    ])
  },

  methods: { 
    cancel() {
      const url = `${process.env.API_URL}/pending/${this.pk}/`
      console.log(url)
      axios.delete(url, this.getConfig)
      .then((res) => { 
        this.$emit('update:promptDialog', false)

        this.snackbar = { 
            text: res.data.return,
            flag: true
        }
      })
    },

    edit() { 

    },

    getMoment(time) { 
      return moment(time, "YYYY-MM-DD hh:mm:ss").fromNow()
    },

    bell(appeal) { 
      this.$emit('update:promptDialog', true)
      const url = `${process.env.API_URL}/pending/`

      axios.post(url, {
        "appeal.session_id": appeal.session_id
      }, this.getConfig)
      .then((res) => { 
        this.pk = res.data.id
      })
    }
  },

  created() { 
  },

  props: { 
    appeal: {
      default: null
    },

    promptDialog: { 
      default: false
    }
  }
}
</script>
