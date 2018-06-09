<template>
  <div>
    <v-dialog v-model="appealPrompt" max-width="290" persistent v-if="request">
      <v-card>
        <v-card-title class="headline">{{ request.helper.username }}</v-card-title>
        <v-card-text>
          is requesting to help you
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn flat="flat" @click="action('approve')">Accept</v-btn>
          <v-btn flat="flat" @click="action('reject')">Decline</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>


<script>
import axios from 'axios'
import {mapGetters} from 'vuex'

export default {
  data() { 
    return { 
      notifications: [],
      page: 1,
      request: null
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
    ])
  },

  methods: { 
    action(action) {
      axios.post(`${process.env.API_URL}/pending/${this.request.id}/update_status/`, {
        action: action
      })
      .then((res) => {
          console.log("RES", res)
          if(action == "approve") {
            this.$router.push(`/session/${res.data.appeal.id}`)
          }
      })
    },

    getNotifications() {
      axios.get(`${process.env.API_URL}/notification/?page=1`, this.getConfig)
      .then((res) => {
          const help = res.data.helper
          if(help != null) { 
              if(help.status == "a") {
                this.$emit('update:promptDialog', false)
                this.$router.push(`/session/${help.appeal.id}`)
              } else if(help.status == "r"){ 
                  if(this.promptDialog == true) { 
                    axios.delete(`${process.env.API_URL}/pending/${help.id}/`, this.getConfig)
                    .then((res) => { 
                      this.$emit('update:promptDialog', false)
                    })
                  }
              }
          }

          this.$emit("update:notifList", res.data.notification)
          this.request = res.data.request
          setTimeout(this.getNotifications, 5600)
      })
      .catch((err) => {
          console.log(err)
      })
    },
  },

  created() { 
    this.getNotifications()
  },

  props: { 
    promptDialog: { 
      type: Boolean
    },

    notifList: { 
      type: Array,
    }
  }
}
</script>
