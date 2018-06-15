<template>
  <div>
    <v-container fill-height pa-0>
      <v-layout justify-center row wrap>
        <v-flex xs8>
          <v-card-text class="text-xs-center">
            <v-btn depressed color="red darken-1" dark @click="stopStream">Close Appeal</v-btn>
          </v-card-text>
        </v-flex>
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

      <v-dialog v-model="prompt" transition="fade-transition" persistent style="border-radius: 15px;" max-width="300">
        <v-card>
           <v-card-text>
             <v-layout justify-center>
               <v-flex text-xs-center>
                 <v-card-text>
                   <v-avatar style="position: relative; left: 5px;">
                     <v-icon size="25">fas fa-users</v-icon>
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

      <rater v-if="ratingDialog" :flag.sync="ratingDialog" :appealID="$route.params.id" :helperName="helperName" :userID="helperID" :redirectTo="`/`" />
    </v-container>
  </div>
</template>

<script>
import Publisher from '../.././components/Publisher'
import Subscriber from '../.././components/Subscriber'
import Rater from '../../components/Rating'

import OT from '@opentok/client'
import axios from 'axios'
import {mapState, mapGetters} from 'vuex'

const errorHandler = (err) => {
  // alert(err.message);
};

export default {
  data() {
    return { 
      "SESSION_ID": "",
      "TOKEN_ID": "",
      loaded: false,
      streams: [],
      session: null,
      ratingDialog: false,
      message: "",       
      chatLog: [],

      prompt: true,

      ownerName: "",
      ownerID: "",
      helperName: "",
      helperID: "",
      publisherName: "",
      subscriberName: "",
      comment: "",

      requestTitle: "",
      requestDetail: "",
    }
  },
  components: { 
    Publisher,
    Subscriber,
    Rater
  },
  created() { 
    axios.get(`${process.env.API_URL}/request/${this.$route.params.id}/`, this.getConfig)
    .then((res) => { 
      this.ownerName = res.data.owner.username
      this.ownerID = res.data.owner.id
      this.helperName = res.data.helper.username
      this.helperID = res.data.helper.id
      this.SESSION_ID = res.data.session_id
      this.TOKEN_ID = res.data.token
      this.requestTitle = res.data.request_title
      this.requestDetail = res.data.detail
      this.initStream()
    })
    .catch((err) => { 
      this.$router.push("/NotFound")
    })

    window.onbeforeunload = function(e) {
      let dialogText = null
      this.stopStream()
      return dialogText;
    }
  },

  computed: { 
    ...mapGetters('userModule', [
      'getConfig'
    ]),

    ...mapState('userModule', [
      'username', 'profilePic', 'userID'
    ])
  },

  methods: {
    errorHandler,
    initStream() { 
      this.session = OT.initSession(process.env.API_KEY, this.SESSION_ID);
      
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
      
      this.session.on('streamCreated', (event) => {
        this.streams.push(event.stream)
        this.prompt = false
      })
      
      this.session.on('streamDestroyed', (event) => {
        const idx = this.streams.indexOf(event.stream);

        this.stopStream()
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
            // console.log(error.name, error.message)
          }else { 
            self.message = ""
          }
        })
      }
    },

    stopStream() {
      this.session.disconnect()
      axios.post(`${process.env.API_URL}/request/${this.$route.params.id}/update_status/`, {
        action: "complete"
      }, this.getConfig)
      .then((res) => { 
        if(this.userID == this.ownerID)
          this.ratingDialog = true
        else { 
          //session ends
          this.$router.push('/appeals/list')
        }
      })
    },
    sendMessage() { 
      this.chatLog.push({text: this.message})
    },
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