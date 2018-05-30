<template>
  <div>
    <app-nav/>
    <v-container>
      <v-layout justify-center>
        <v-flex xs12 sm12 md12 lg4 xl4>
          <v-card class="pa-3">
            <v-card-text>
              <h3 class="headline text-xs-center">Create a new appeal</h3>
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

              <v-btn @click="send" :loading="isLoading">
                Send
              </v-btn>
            </v-card-text>
          </v-card>
        </v-flex>
        
      </v-layout>
      <snackbar :snackbar="snackbar"/>
    </v-container>
  </div>
</template>

<script>
//Components
import appNav from '../../components/AppNav.vue'
import snackbar from '../../components/Snackbar.vue'

//Plugins
import axios from 'axios'

export default {
  data() { 
    return { 
      request_title: "",
      detail: "",
      isLoading: false,

      snackbar: {}
    }
  },

  components: { 
    appNav,
    snackbar
  },

  methods: { 
    send() { 
      const config = { 
        headers: { 
          Authorization: `Token ${localStorage.getItem("token")}`
        }
      }

      this.isLoading = true

      axios.post(`${process.env.API_URL}/request/`, {
        request_title: this.request_title,
        detail: this.detail
      }, config)

      .then((res) => { 
        this.isLoading = false
        
        this.snackbar = { 
          text: res.data.return,
          flag: true,
        }

        this.request_title = ""
        this.detail = ""
      })

      .catch((res) => { 
        this.snackbar = { 
          text: "An error has occured",
          flag: true,
        }
      })
    }
  },

  test() { 
    const config = { 
        headers: { 
          Authorization: `Token ${localStorage.getItem("token")}`
        }
      }

    axios.patch(`${process.env.API_URL}/request/19/`, {
      "request_title": "CHANGED",
      "detail": "detail change"
    }, config)

    .then((res)=>{
      console.log("nice")
    })

    .catch((err) => { 
      console.log(err)
    })
  }
}
</script>
