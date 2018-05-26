<template>
  <v-container grid-list-lg>
    <v-layout row justify-center> 
      <v-flex xs8 sm6 md5 lg5 xl12 mt-5>
          <v-card class="pa-4">
              <v-form class="ma-2">
                  <v-text-field
                      label="Username"
                      v-model="username"
                  ></v-text-field>
                  <v-text-field
                      label="Password"
                      v-model="password"
                      :append-icon="seePass ? 'visibility_off' : 'visibility'"
                      :append-icon-cb="() => (seePass = !seePass)"
                      :type="seePass ? 'text' : 'password'"
                  
                  ></v-text-field>

                  <v-layout>
                    <v-flex xs12 sm12 md6>
                      <v-text-field
                          label="First Name"
                          v-model="first_name"
                      ></v-text-field>
                    </v-flex>

                    <v-flex xs12 sm12 md6>
                      <v-text-field
                          label="Last Name"
                          v-model="last_name"
                      ></v-text-field>
                    </v-flex>
                    
                  </v-layout>
                  <v-select
                    v-model="gender"
                    :items="genderList"
                    label="Gender"
                    single-line>
                  </v-select>
                  <v-btn color="success" @click="register()">Register</v-btn>
              </v-form>
          </v-card>
      </v-flex>
  </v-layout>
  </v-container>
</template>

<script>
import axios from 'axios'

export default {
    data() { 
        return { 
            username: "",
            password: "",
            first_name: "",
            last_name: "",
            gender: "",
            seePass: false,
            genderList: [
              {text: "Male"},
              {text: "Female"}
            ]
        }
    },

    methods: { 
        register() {
            axios.post("http://192.168.1.2:8000/user/", {
                username: this.username,
                password: this.password,
                first_name: this.first_name,
                last_name: this.last_name,
                gender: this.gender.text

            })

            .then((res) => { 
              if(res.data.return == "Account successfully created.") { 
                this.$router.push("/login")
              }
            })

            .catch((err) => { 
                console.log(err)
            })
        }
    },

    beforeCreate() { 
        if(localStorage.getItem("token") != null) { 
            this.$router.push("/")
        }
    }
}
</script>
