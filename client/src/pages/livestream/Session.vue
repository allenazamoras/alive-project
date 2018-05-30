<template>
  <div>
    <app-nav/>
    <v-container grid-list-xl>
      <v-layout row wrap justify-center>
        <v-flex md8 lg8 xl6>
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
      </v-layout>

      <v-dialog v-model="dialog" max-width="290" persistent>
      <v-card>
        <v-card-title class="headline">How was the session?</v-card-title>
        <v-card-text>
        <v-text-field v-model="rating">

        </v-text-field>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="green darken-1" flat="flat" @click="rate">Rate</v-btn>
        </v-card-actions>
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

const errorHandler = (err) => {
  alert(err.message);
};

export default {
  data() {
    return { 
      "API_KEY": '46116232',
      "SESSION_ID": "1_MX40NjExNjIzMn5-MTUyNjg3MzM0ODU3MH5aUGZQL1lnSi9UTm5hcTRrN25TRjRkcUJ-fg",
      "TOKEN_ID": "T1==cGFydG5lcl9pZD00NjExNjIzMiZzaWc9ZDViOGQ5NGMxYTBiM2NjMTg4YWU1YzcyOGFmZDM2OGUzMzUyNzAwZTppbml0aWFsX2xheW91dF9jbGFzc19saXN0PSZleHBpcmVfdGltZT0xNTI3NzU1NjIzJmNyZWF0ZV90aW1lPTE1Mjc2NjkyMjMmcm9sZT1wdWJsaXNoZXImbm9uY2U9OTM1NzQ2JnNlc3Npb25faWQ9MV9NWDQwTmpFeE5qSXpNbjUtTVRVeU5qZzNNek0wT0RVM01INWFVR1pRTDFsblNpOVVUbTVoY1RSck4yNVRSalJrY1VKLWZn",
      
      loaded: false,
      streams: [],
      session: null,
      dialog: false,
      rating: 0,
      message: "",
      chatLog: [],

      requestTitle: "",
      requestDetail: "",
    }
  },

  created () {
    axios.get(`${process.env.API_URL}/request/${this.$store.state.session.appealID}/`, this.$store.state.user.config)
    .then((res) => { 
      this.API_KEY = '46116232'
      this.SESSION_ID = res.data.session_id
      this.TOKEN_ID = res.data.opentok_token
      this.requestTitle = res.data.request_title
      this.requestDetail = res.data.detail
      this.initStream()
    })
  },


  methods: {
    errorHandler,

    initStream() { 
      this.session = OT.initSession(this.API_KEY, this.SESSION_ID);
      console.log(this.session);
      this.session.connect(this.TOKEN_ID, (err) => {
        console.log('connect callback');
        if (err) {
          errorHandler(err);
        }
      });
      this.session.on('streamCreated', (event) => {
        console.log(event)
          this.streams.push(event.stream);

        console.log(this.streams)
      });
      this.session.on('streamDestroyed', (event) => {
        const idx = this.streams.indexOf(event.stream);
        if (idx > -1) {
          this.streams.splice(idx, 1);
        }
      });
    },

    rate() { 
      axios.post(`${process.env.API_URL}/rating/`, {
        "user": 1,
        "appeal": 19,
        "rating": this.rating,
      }, this.$store.user.config)

      .then((res) => { 
        this.dialog = false
      })

      .catch((res) => {
        console.log(res)
      })
    },

    stopStream() { 
      this.session.disconnect()
    },

    sendMessage() { 
      this.chatLog.push({text: this.message})
    }
  },

  components: { 
    appNav,
    Publisher,
    Subscriber

  }
}
</script>