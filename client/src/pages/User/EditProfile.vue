<template>
  <div>
    <v-container 
        grid-list-xl
    >
      <v-layout
        row
        wrap
        justify-center
      >
        <v-flex
          xs12
          sm9
          md4
          lg5
        >
          <v-card
            class="pa-3"
          >
            <v-card-title class="pb-0">
              <v-subheader  class="pl-0"><v-icon size="12">fas fa-user fa-fw</v-icon> Profile Settings</v-subheader>
            </v-card-title>
            <v-fade-transition>
              <v-card-text v-show="alertPrompt.flag">
                <v-alert outline :value="alertPrompt.flag" :color="alertPrompt.color" :icon="alertPrompt.icon">
                  {{alertPrompt.text}}
                </v-alert>
              </v-card-text>
            </v-fade-transition>
            <v-card-text class="text-xs-center">
              <v-avatar size="100">
                <img :src="api_url + user.profile_picture_url" alt="">

              </v-avatar>
            </v-card-text>
            <v-card-text class="pt-0">
              <v-form
                ref="form"
                v-model="valid"
              >
                <v-text-field
                  v-model="user.username"
                  label="Username"
                  @change="update('username')"
                ></v-text-field>
                <v-layout>
                  <v-flex>
                    <v-text-field
                      v-model="user.first_name"
                      label="First Name"
                      @change="update('first_name')"
                    ></v-text-field>
                  </v-flex>
                  <v-flex>
                    <v-text-field
                      v-model="user.last_name"
                      label="Last Name"
                      @change="update('last_name')"
                    ></v-text-field>
                  </v-flex>
                </v-layout>
                <v-select
                  v-model="user.gender"
                  :items="genderList"
                  label="Gender"
                  single-line
                  @change="update('gender')"
                >
                </v-select>
                <v-text-field
                  type="password"
                  label="New password"
                  v-model="user.password"
                  @change="update('password')"
                ></v-text-field>
                <v-btn @click="updateProfile" depressed round color="indigo" :loading="updateLoading" dark>Update</v-btn>
              </v-form>
            </v-card-text>
          </v-card>
        </v-flex>
      </v-layout>

      <v-dialog max-width="300" v-model="passwordPrompt">
        <v-card tile class="pa-2">
          <v-card-title>
            <span>
              Enter password to confirm changes
            </span>
          </v-card-title>
          <v-card-text>
            <v-form
              ref="passwordForm"
            > 
              <v-text-field
                :rules="passwordRules"
                label="Current password"
                type="password"
                v-model="updateData['confirm_password']"
              ></v-text-field>
                <v-btn 
                round
                block
                outline
                depressed
                color="success"
                @click="send"
              >
                Confirm
              </v-btn>
            </v-form>
          </v-card-text>
        </v-card>
      </v-dialog>
    </v-container>
  </div>
</template>

<script>
import {mapState, mapGetters} from 'vuex'
import axios from 'axios'

export default {
  data() { 
    return { 
      passwordPrompt: false,
      updateLoading: false,
      api_url: process.env.API_URL,
      valid: true,
      alertPrompt: { 
        text: "",
        icon: "",
        flag: false,
        color: ""
      },
      dialog: false,
      userDefault: { 
        username: "",
        gender: "",
        first_name: "",
        last_name: ""
      },
      user: { 
        username: "",
        gender: "",
        first_name: "",
        last_name: ""
      },

      updateData: {},
      password: "",
      passwordRules: [
          v => !!v || 'Password is required',
          v => (v && v.length > 6) || 'Password must be more than 6 characters.'
      ],
      genderList: [
        "Male", "Female"
      ]
    }
  },

  created() { 
    this.getUserData()
  },  

  computed: {
    ...mapState('userModule', [
      'userID'
    ]),

    ...mapGetters('userModule', [
      'getConfig'
    ])
  },

  methods: { 
    //Updates the updateData object with the new values as long as it's not blank.
    update(field) {
      this.$nextTick(() => { 
        this.$set(this.user, field, this.user[field].replace(/\s+/g, ''))
        if(this.user[field] == this.userDefault[field] || this.user[field] == "") {
          if(this.updateData[field] != null) { 
            this.$delete(this.updateData, field)
          }
        } else { 
          this.$set(this.updateData, field, this.user[field])
        }
      })
    },

    updatePassword() { 
      if(Object.keys(this.updateData).length === 0 && this.updateData.constructor === Object) { 
        this.alertPrompt = {
          flag: true,
          color: "warning",
          icon: "priority_high",
          text: "There were no changes so nothing was updated."
        }
      } else { 
        //send
        this.warningFlag = false
        this.send()
      }
    },

    updateProfile() {
      if(Object.keys(this.updateData).length === 0 && this.updateData.constructor === Object) { 
        this.alertPrompt = {
          flag: true,
          color: "warning",
          icon: "priority_high",
          text: "There were no changes so nothing was updated."
        }
      } else { 
        //send
        this.warningFlag = false
        if(this.updateData['password'] == null) { 
          this.$set(this.updateData, 'password', '')
        }
        this.$set(this.updateData, 'confirm_password', '')
        
        this.passwordPrompt = true
      }
    },

    send() { 
      if(this.$refs.passwordForm.validate()) {
        axios.patch(`${process.env.API_URL}/user/${this.userID}/`, this.updateData, this.getConfig)
        .then((res) => {
          console.log(res)
          this.passwordPrompt = false
          if(res.data.return == "Incorrect password") { 
            this.alertPrompt = {
              flag: true,
              color: "red",
              icon: "priority_high",
              text: "Incorrect password"
            }
          } else { 
            this.getUserData()
            this.updateLoading = false
            this.alertPrompt = {
              flag: true,
              color: "success",
              icon: "check_circle",
              text: "Successfully updated profile!"
            }
          }
        })
        .catch((err) => { 
          console.log(err)
        })
      }
    },

    getUserData() { 
      axios.get(`${process.env.API_URL}/user/${this.userID}/`, this.getConfig)
      .then((res) => { 
        this.userDefault = res.data
        this.$set(this.userDefault, 'current_password', '')
        this.$set(this.userDefault, 'password', '')
        this.user = Object.assign({}, this.userDefault)
      })
    }
  }
}
</script>
