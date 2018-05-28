<template>
  <div>
    <app-nav/>
    <v-container>
      <v-layout justify-center>
        <v-flex xs12 sm12 md12 lg4 xl4>
          <v-card>
            <v-card-text>
              <v-form>
                <v-text-field
                    label="Title"
                    v-model="request_title"
                ></v-text-field>
                <v-text-field
                    label="Detail"
                    multi-line
                    v-model="detail"
                ></v-text-field>
              </v-form>

              <v-btn @click="send()">
                Send
              </v-btn>
            </v-card-text>
          </v-card>
        </v-flex>
        
      </v-layout>
    </v-container>
  </div>
</template>

<script>
import appNav from '../../components/AppNav.vue'
import axios from 'axios'

export default {
  data() { 
    return { 
      request_title: "",
      detail: ""
    }
  },

  components: { 
    appNav
  },

  methods: { 
    send() { 
      const config = { 
        headers: { 
          Authorization: `Token ${localStorage.getItem("token")}`
        }
      }

      axios.post(`${process.env.API_URL}/request/`, {
        request_title: this.request_title,
        detail: this.detail
      }, config)

      .then((res) => { 
        console.log("NICE")
      })
    }
  },

  created() { 
  }
}
</script>