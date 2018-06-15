<template>
  <div>
    <v-dialog v-model="appealPrompt" max-width="300" persistent v-if="request">
      <v-card>
        <v-card-text class="text-xs-center">
          <v-avatar size="25">
            <img :src="api_url + request.helper.profile_picture" alt="">
          </v-avatar>
          <span class="subheading">{{ request.helper.first_name + " " + request.helper.last_name }}
          is requesting to help you.</span>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn 
            depressed 
            @click="action('approve')"
            round
            dark
            color="green"
          >
            <v-icon size="15">fas fa-phone fa-fw</v-icon>
            Accept
          </v-btn>
          <v-btn 
            depressed 
            @click="action('reject')"
            round
            dark
            color="red"
          >
            <v-icon size="15">fas fa-phone-slash fa-fw</v-icon>
            Decline
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>


<script>
import axios from 'axios'
import {mapState, mapMutations, mapGetters} from 'vuex'

export default {
  data() { 
    return { 
      helper: null,
      notifications: [],
      page: 1,
      request: null,
      api_url: process.env.API_URL,
      acceptIsLoading: false,
      rejectIsLoading: false,
    }
  },

  computed: { 
    appealPrompt: { 
      get() {
        return this.request != null ? true: false
      }
    },
    ...mapGetters('userModule', [
      'getConfig'
    ]),
    ...mapState('dialogModule', [
      'flag'
    ])
  },

  methods: { 
    action(action) {
      if(action == 'approve') { 
        this.acceptIsLoading = true
      } else if(action == 'reject'){ 
        this.rejectIsLoading = true
      }

      axios.post(`${process.env.API_URL}/pending/${this.request.id}/update_status/`, {
        action: action
      })
      .then((res) => {
        if(action == "approve") {
          this.$router.push(`/session/${res.data.appeal.id}`)
          this.acceptIsLoading = false
        }
      })
      .catch((res) => { 
        this.setFlag(false)
      })
    },

    getNotifications() {
      axios.get(`${process.env.API_URL}/notification/?page=1`, this.getConfig)
      .then((res) => {
        console.log(res.data.helper)
          const help = res.data.helper

          if(help.status != null) { 
            if(help.status == "a") {
              this.setFlag(false)
              this.$router.push(`/session/${help.appeal.id}`)
            } else if(help.status == "r"){ 
                if(this.flag == true) { 
                  axios.delete(`${process.env.API_URL}/pending/${help.id}/`, this.getConfig)
                  .then((res) => { 
                    this.setFlag(false)
                  })
                }
            }
          }

          this.$emit("update:notifList", res.data.notification)
          this.request = res.data.request
          setTimeout(this.getNotifications, 2000)
      })
      .catch((err) => {
          console.log(err)
      })
    },
    ...mapMutations('dialogModule', [
      'setFlag'
    ])
  },

  created() { 
    this.getNotifications()
  },

  props: { 
    notifList: { 
      type: Array,
    }
  }
}
</script>
