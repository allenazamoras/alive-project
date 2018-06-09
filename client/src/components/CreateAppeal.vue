<template>
  <div>
    <v-dialog v-model="createDialog" max-width="400" persistent>
        <v-card class="pt-3 pb-3">
            <v-card-text class="text-xs-center">
                <moon/>
            </v-card-text>
            <v-card-text class="body-1 text-xs-center grey--text text--darken-2">
              There are times when we feel alone. Don't worry, you're not!
            </v-card-text>

            <v-card-text>
                <v-form 
                  v-model="valid" 
                  ref="form" 
                  lazy-vaidation>
                  <v-text-field 
                    counter="50"
                    required 
                    label="Title" 
                    :rules="titleRules"
                    placeholder="Describe it in a few words." 
                    v-model="request_title"
                  ></v-text-field>
                  <v-text-field 
                    counter="500"
                    required 
                    multi-line 
                    label="Detail" 
                    :rules="detailRules"
                    placeholder="And expound it more here." 
                    v-model="detail"
                  ></v-text-field>
                  <v-select
                    :items="categories"
                    v-model="category"
                    label="Select a category"
                    required
                  ></v-select>
                </v-form>
                
            </v-card-text>
            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn flat="flat" @click="send" :loading="isLoading">Post</v-btn>
                <v-btn flat="flat" @click="$emit('update:createDialog', false)">Cancel</v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
    <snackbar :snackbar="snackbar"/>
  </div>
</template>

<script>
import moon from './Moon'
import snackbar from './Snackbar'

//Plugins
import axios from 'axios'
import {mapGetters} from 'vuex'

export default {
  data() { 
    return { 
      request_title: "",
      detail: "",
      isLoading: false,

      valid: true,

      snackbar: {},

      categories: ['OTHER', 'SCHOOL', 'FAMILY', 'RELATIONSHIPS', 'PERSONAL', 'WORK'],
      category: "OTHER",

      titleRules: [
        v => !!v || 'Title is required',
        v => (v && v.length <= 50) || 'Title must be less than 51 characters'
      ],

      detailRules: [
        v => !!v || 'Detail is required',
        v => (v && v.length <= 500) || 'Detail must be less than 501 characters'
      ]
    }
  },

  computed: { 
    ...mapGetters('userModule', [
      'getConfig'
    ])
  },

  methods: { 
    send() { 
      if(this.$refs.form.validate()) { 
        this.isLoading = true
        axios.post(`${process.env.API_URL}/request/`, {
          request_title: this.request_title,
          detail: this.detail,
          category: this.category
        }, this.getConfig)

        .then((res) => { 
          this.isLoading = false
          if(res.data.return == "Successfully created new request") { 
            this.$emit('update:createDialog', false)
          }

          this.snackbar = { 
            text: res.data.return,
            flag: true,
          }
        })

        .catch((res) => { 
          console.log(res)
          this.loading = false
          this.snackbar = { 
            text: "An error has occured",
            flag: true,
          }
        })
      }
      
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
  },

  props: { 
    createDialog: { 
      type: Boolean,
      default: false
    }
  },

  components: { 
    moon,
    snackbar
  }
}
</script>
