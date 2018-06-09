<template>
  <div>
    <app-nav/>
    <v-container fill-height pa-0>
      <v-layout justify-center row wrap>
        <v-flex v-if="session" xs8 pb-0>
          <div id="session" @error="errorHandler">
            <div id="subscribers" v-for="(stream, index) in streams" :key="stream.streamId" v-if="index < 1">
              <subscriber @error="errorHandler" :name="subscriberName" :stream="stream" :session="session"></subscriber>
            </div>
          </div>
          
          <publisher :session="session" @error="errorHandler"></publisher>
        </v-flex>
        <v-flex xs8 pa-0 class="chatbox">
          <v-layout
            row
            wrap
            justify-center
          >
            <v-flex xs12>
              <v-card height="25vh" style="overflow-y: auto; overflow-x: none;">
                <v-card-text>
                  <div id="messages"></div>          
                </v-card-text>
              </v-card>
            </v-flex>
            <v-flex xs12>
              <v-card>
                <v-card-text>
                  <v-text-field placeholder="Type something here" v-model="message" append-icon="send" @keyup.enter="send"></v-text-field>
                </v-card-text>
              </v-card>
            </v-flex>
          </v-layout>
        </v-flex>
      </v-layout>

      <!-- <v-dialog v-model="dialog" max-width="290" persistent>
        <v-card>
          <v-card-title class="headline">How was the session?</v-card-title>
          <v-card-text>
          <v-text-field placeholder="rating number" v-model="rating"></v-text-field>
          <v-text-field placeholder="Describe what you thought." v-model="comment" multi-line counter="255"></v-text-field>
          <v-btn color="green darken-1" outline round dark block @click="rate">Rate</v-btn>
          </v-card-text>
        </v-card>
      </v-dialog> -->

      <v-dialog v-model="prompt" transition="fade-transition" persistent style="border-radius: 15px;" max-width="300">
        <v-card>
           <v-card-text>
             <v-layout justify-center>
               <v-flex text-xs-center>
                 <v-card-text>
                   <v-avatar style="position: relative; left: 5px;">
                     <v-icon size="25">fas fa-users</v-icon>
                     <!-- <img :src="profilePic" alt=""> -->
                   </v-avatar>
                   <br>
                  <span class="headline grey--text text--darken-2">Waiting for lobby to be filled.</span>
                 </v-card-text>
                 
                 <v-btn depressed color="red darken-1" dark @click="stopStream">Close Appeal</v-btn>
               </v-flex>
             </v-layout>
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

      prompt: true,

      ownerName: "",
      helperName: "",
      publisherName: "",
      subscriberName: "",
      comment: "",

      requestTitle: "",
      requestDetail: "",
    }
  },

  created() { 
    axios.get(`${process.env.API_URL}/request/${this.$route.params.id}/`, this.getConfig)
    .then((res) => { 
      console.log(res)
      this.ownerName = res.data.owner.username
      this.helperName = res.data.helper.username
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
      'username', 'profilePic'
    ])
  },

  methods: {
    errorHandler,

    initStream() { 
      this.session = OT.initSession(process.env.API_KEY, this.SESSION_ID);
      debugger;
      this.session.connect(this.TOKEN_ID, (err) => {
        if (err) {
          errorHandler(err)
        }else { 
          self = this
          this.session.on('signal:msg', function signalCallback(event) {
            let person = event.from.connectionId === self.session.connection.connectionId ? 'You' : 'Other'

            const orientation = (person == 'You') ? 'right': 'left'
            let text = {message: event.data, orientation: orientation}
            let messages = document.querySelector('#messages')
            let msg = document.createElement('p')
            let identifier = ""
            let sender = ""
            
            if((self.ownerName != self.username)) { 
              self.publisherName = self.helperName
              self.subscriberName = self.ownerName
            } else { 
              self.publisherName = self.ownerName
              self.subscriberName = self.helperName
            }

            sender = (person == 'You') ? self.publisherName: self.subscriberName
            
            messages.classList.add('pa-0')
            msg.className = person
            msg.style.marginBottom = "0px"
            msg.style.marginTop = "16px"

            identifier = `<span class="caption" style="font-weight: bold;">${sender}</span><br>`

            if(messages.lastChild != null) { 
              if(messages.lastChild.classList.contains(person)) {
                identifier = ""
                msg.style.marginTop = "0px"
              }
            } else { 
              msg.style.marginTop = "0px"
            }

            msg.innerHTML = identifier + event.data
            messages.appendChild(msg)
            msg.scrollIntoView()
          })
        }
      })
      debugger;
      this.session.on('streamCreated', (event) => {
        this.streams.push(event.stream)
        this.prompt = false
      })
      debugger;
      this.session.on('streamDestroyed', (event) => {
        const idx = this.streams.indexOf(event.stream);

        if (idx > -1) {
          this.streams.splice(idx, 1)
          this.prompt = true
        }
      })
    },

    send() { 
      self = this

      if(self.message.length > 0) { 
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
      }
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

<style>
  .md-chip {
    display: inline-block;
    background: #e0e0e0;
    padding: 0 12px;
    border-radius: 32px;
    font-size: 13px;
  }
  .chatbox {
    position: relative;
    bottom: 72px;
  }

  .OT_publisher {
    position: relative;
    bottom: 90px;
    left: 18px;
    border: 3px solid white;
    border-radius: 3px;
  }
</style>