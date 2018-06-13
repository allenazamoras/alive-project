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
          sm4
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
                <img :src="user.profile_picture" alt="">

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
                <v-btn @click="updateProfile" depressed round color="indigo" :loading="updateLoading" dark>Update</v-btn>
              </v-form>
            </v-card-text>
            <v-divider></v-divider>
            <v-card-text>
              <v-subheader  class="pl-0"><v-icon size="12">fas fa-key fa-fw</v-icon> Change Password</v-subheader>
              <v-form
                ref="changePassword"
              >
                <v-text-field
                  type="password"
                  label="Current password"
                  v-model="user.confirm_password"
                  @change="update('confirm_password')"
                ></v-text-field>
                <v-text-field
                  type="password"
                  label="New password"
                  v-model="user.password"
                  @change="update('password')"
                ></v-text-field>
                <v-btn @click="updatePassword" round depressed dark>Change Password</v-btn>
              </v-form>
            </v-card-text>
          </v-card>
        </v-flex>
      </v-layout>
    </v-container>
  </div>
</template>

<script>
import {mapState, mapGetters} from 'vuex'
import axios from 'axios'

export default {
  data() { 
    return { 
      updateLoading: false,
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
        this.$set(this.updateData, 'confirm_password', '')
        this.$set(this.updateData, 'password', '')
        this.send()
      }
    },

    send() { 
      this.updateLoading = true

      axios.patch(`${process.env.API_URL}/user/${this.userID}/`, this.updateData, this.getConfig)
      .then((res) => { 
        console.log(res)
        this.getUserData()
        this.updateLoading = false
        this.alertPrompt = {
          flag: true,
          color: "success",
          icon: "check_circle",
          text: "Successfully updated profile!"
        }
      })
      .catch((err) => { 
        console.log(err)
      })
    },

    getUserData() { 
      axios.get(`${process.env.API_URL}/user/${this.userID}`, this.getConfig)
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
