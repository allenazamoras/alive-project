<template>
  <div>
    <v-dialog v-model="dialogFlag" max-width="600">
      <v-stepper v-model="currStep">
        <v-stepper-header>
          <v-stepper-step :complete="currStep > 1" step="1">Welcome</v-stepper-step>
          <v-divider></v-divider>
          <v-stepper-step 
            :complete="currStep > 2" 
            step="2"
            :rules="[() => step1Flag]"
          >What are you going through?</v-stepper-step>
          <v-divider></v-divider>
          <v-stepper-step step="3">Nature of the problem</v-stepper-step>
        </v-stepper-header>
        <v-stepper-items>
          <v-stepper-content step="1">
              <v-card-text class="text-xs-center">
                <moon/>
              </v-card-text>
              <v-card-text class="subheading text-xs-center grey--text text--darken-2">
                There are times when we feel alone. Don't worry, you're not!
              </v-card-text>
          </v-stepper-content>
          <v-stepper-content step="2">
            <v-card class="elevation-0">
              <v-card-text class="text-xs-center">
                What are you going through?
              </v-card-text>
              <v-card-text>
                <v-form 
                  v-model="valid" 
                  ref="step1" 
                  lazy-vaidation
                >
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
                </v-form>
              </v-card-text>
            </v-card>
          </v-stepper-content>
          <v-stepper-content step="3">
            <v-card class="elevation-0">
              <v-card-text class="text-xs-center">
                Which best describes the nature of your problem?
              </v-card-text>
              <v-form
                v-model="valid"
                ref="step3"
                lazy-validation
              >
                <v-select
                  :rules="categoryRules"
                  :items="categories"
                  item-text="name"
                  item-value="id"
                  v-model="category"
                  label="Select a category"
                  required
                ></v-select>
              </v-form>
            </v-card>
          </v-stepper-content>
        </v-stepper-items>
      </v-stepper>
        <v-card class="pt-3 pb-3">
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn 
              depressed
              dark
              round
              :color="leftButton.color"
              @click="nextStep" 
              :loading="isLoading"
            >{{leftButton.text}}</v-btn>
            <v-btn 
              depressed
              round
              :color="rightButton.color"
              @click="prevStep"
            >{{rightButton.text}}</v-btn>
          </v-card-actions>
        </v-card>
    </v-dialog>
    <snackbar :snackbar="snackbar"/>
  </div>
</template>

<script>
//Components
import moon from './Moon'
import snackbar from './Snackbar'

//Plugins
import axios from 'axios'
import {mapGetters} from 'vuex'

export default {
  data() { 
    return { 
      lBtn: "Continue",
      rBtn: "Cancel",
      currStep: 0,
      request_title: "",
      detail: "",
      isLoading: false,

      step1Flag: true,
      step3Flag: true,

      valid: true,

      snackbar: {},
      category: -1,
      categories: [],

      titleRules: [
        v => !!v || 'Title is required',
        v => (v && v.length <= 50) || 'Title must be less than 51 characters'
      ],

      detailRules: [
        v => !!v || 'Detail is required',
        v => (v && v.length <= 500) || 'Detail must be less than 501 characters'
      ],

      categoryRules: [
        () => (this.category == -1) ? 'Category is required.': true
      ]
    }
  },
  components: { 
    moon,
    snackbar
  },
  created() { 
    axios.get(`${process.env.API_URL}/category/`, this.getConfig)
    .then((res) => { 
      this.categories = res.data.results
    })
  },
  computed: {
    dialogFlag: { 
      set(val) { 
        this.$emit('update:createDialog', val)
      },
      get() { 
        return this.createDialog
      }
    },
    leftButton() { 
      let ret = {
        text: "Continue",
        color: "indigo"
      }

      if(this.currStep == 2) { 
        ret.text = "Next"
      } else if(this.currStep == 3) { 
        ret.text = "Finish"
        ret.color = "success"
      }

      return ret
    },
    rightButton() { 
      let ret = { 
        text: "Cancel",
        color: "grey lighten-3"
      }

      if(this.currStep > 1) { 
        ret.text = "Previous"
      }

      return ret
    },
    ...mapGetters('userModule', [
      'getConfig'
    ])
  },
  methods: { 
    nextStep() { 
      if(this.currStep < 3) { 
        if(this.currStep == 2) { 
          if(this.$refs.step1.validate()) {
            this.currStep++
            if(!this.step1Flag) { 
              this.step1Flag = true
            }
          } else { 
            this.step1Flag = false
          }
        } else { 
          this.currStep++
        }
      } else { 
        if(this.$refs.step3.validate()) { 
          this.send()
          this.step3Flag = true
        } else { 
          this.step3Flag = false
        }
      }
    },

    prevStep() { 
      if(this.currStep > 1) { 
        this.currStep--
      } else { 
        this.$emit("update:createDialog", false)
      }
      
    },

    send() { 
      this.isLoading = true
      axios.post(`${process.env.API_URL}/request/`, {
        request_title: this.request_title,
        detail: this.detail,
        category: this.category
      }, this.getConfig)
      .then((res) => {
        console.log(res)
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
        this.loading = false
        this.snackbar = { 
          text: res.data.statusText,
          flag: true,
        }
      })
    }
  },

  props: { 
    createDialog: { 
      type: Boolean,
      default: false
    }
  },
}
</script>
