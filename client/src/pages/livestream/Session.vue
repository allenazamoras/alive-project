<template>
  <div>
    <app-nav/>
    <v-container grid-list-xl>
      <v-layout row wrap justify-center>
        <v-flex xs12 sm12 md8 lg8 xl6>
          <v-layout column>
            <v-flex xs12>
              <h3>{{ requestTitle }}</h3>
              <h4>{{ requestDetail }}</h4>
              <v-btn class="red white--text" @click="stopStream">End Session</v-btn>
              <div id="session" @error="errorHandler">
                <div id="subscribers" v-for="(stream, index) in streams" :key="stream.streamId" v-if="index < 1">
                  <subscriber v-if="session" @error="errorHandler" :stream="stream" :session="session"></subscriber>
                </div>
              </div>
            </v-flex>

            <v-flex xs12>
              <publisher v-if="session" :session="session" @error="errorHandler"></publisher>
            </v-flex>
          </v-layout>
        </v-flex>
        <v-flex xs12 sm12 md4 lg4 xl6>
          <v-card>
            <v-card-text>
              <v-layout row>
                <v-flex>
                  <div style="overflow: auto; height: 50vh;">
                    <div v-for="chat in chatLog">
                      <v-chip color="blue" disabled text-color="white">
                        {{chat}}
                      </v-chip>
                    </div>
                  </div>
                </v-flex>
              </v-layout>
              <v-layout row>
                <v-flex>
                  <v-text-field v-model="message" solo append-icon="send" placeholder="Type your message here" @keyup.enter="send"></v-text-field>
                </v-flex>
              </v-layout>
            </v-card-text>
          </v-card>
        </v-flex>
      </v-layout>

    <v-dialog v-model="dialog" max-width="290" persistent>
        <v-card>
          <v-card-title class="headline">How was the session?</v-card-title>
          <v-card-text>
          <v-text-field placeholder="rating number" v-model="rating"></v-text-field>
          <v-text-field placeholder="Describe what you thought." v-model="comment" multi-line counter="255"></v-text-field>
                    <v-btn>lol</v-btn>
          <v-btn color="green darken-1" outline round dark block @click="rate">Rate</v-btn>
          </v-card-text>
        </v-card>
      </v-dialog>
    </v-container>

  </div>
</template>

<script>
import appNav from '../.././components/AppNav.vue'
import Publisher from '../.././components/Publisher.vue'
import Subscriber from '../.././components/Subscriber.vue'

import OT from '@opentok/client'
import axios from 'axios'
import {mapState, mapGetters} from 'vuex'

const errorHandler = (err) => {
  alert(err.message);
};

export default {
  data() {
    return { 
      "SESSION_ID": "",
      "TOKEN_ID": "",
      
      loaded: false,
      streams: [],
      session: null,
      dialog: false,
      rating: 0,
      message: "",
      chatLog: [],

      owner: "",
      comment: "",

      requestTitle: "",
      requestDetail: "",
    }
  },

  created () {
    axios.get(`${process.env.API_URL}/request/${this.$route.params.id}/`, this.getConfig)
    .then((res) => { 
      this.owner = res.data.owner.username
      this.SESSION_ID = res.data.session_id
      this.TOKEN_ID = res.data.token
      this.requestTitle = res.data.request_title
      this.requestDetail = res.data.detail
      this.initStream()
    })
    .catch((err) => { 
      this.$router.push("/NotFound")
    })
  },

  computed: { 
    ...mapGetters('userModule', [
      'getConfig'
    ]),

    ...mapState('userModule', [
      'username'
    ])
  },

  methods: {
    errorHandler,

    initStream() { 
      this.session = OT.initSession(process.env.API_KEY, this.SESSION_ID);
      this.session.connect(this.TOKEN_ID, (err) => {
        if (err) {
          errorHandler(err);
        }else { 
          self = this
          this.session.on('signal:msg', function signalCallback(event) {
            let person = event.from.connectionId === self.session.connection.connectionId ? 'You' : 'Other dude'
            let text = person + ": " + event.data
            self.chatLog.push(text)
          })
        }
      })
      this.session.on('streamCreated', (event) => {
        this.streams.push(event.stream);
      })
      this.session.on('streamDestroyed', (event) => {
        const idx = this.streams.indexOf(event.stream);
        if (idx > -1) {
          this.streams.splice(idx, 1);
        }
      })
    },

    send() { 
      self = this

      this.session.signal({
        type: 'msg',
        data: self.message
      }, function signalCallback(error) { 
        if(error) {
          console.log(error.name, error.message)
        }else { 
          self.message = ""
        }
      })
    },

    rate() { 
      axios.post(`${process.env.API_URL}/rating/`, {
        "user": 1,
        "appeal": this.$route.params.id,
        "rating": this.rating,
        "comment": this.comment
      }, this.getConfig)

      .then((res) => { 
        this.dialog = false
        console.log(res)
      })

      .catch((res) => {
        console.log(res)
      })
    },

    stopStream() {
      axios.post(`${process.env.API_URL}/request/${this.$route.params.id}/update_status/`, {
        action: "complete"
      }, this.getConfig)
      .then((res) => { 
        this.session.disconnect()

        if(this.owner == this.username) { 
          this.dialog = true
        }
      })
    },

    sendMessage() { 
      this.chatLog.push({text: this.message})
    },
  },

  components: { 
    appNav,
    Publisher,
    Subscriber
  }
}
</script>