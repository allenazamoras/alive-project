<template>
    <main :style="`background-image: url(${patternURL}); background-repeat: repeat;`">
        <v-container fill-height>
            <v-layout align-center justify-center> 
                <v-flex xs10 sm8 md7 lg4 xl3>
                    <v-card class="pa-4 elevation-10">
                        <v-card-text class="headline text-xs-center">
                            Register
                        </v-card-text>
                        <v-form class="pa-4 pb-5">
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
                        </v-form>
                        <v-card-text flex>
                                <v-btn color="primary" @click="register" large>Register</v-btn>
                                <router-link to="/login">Sign in instead</router-link>
                        </v-card-text>
                    </v-card>
                </v-flex>
                <snackbar :snackbar="snackbar"/>         
            </v-layout>
        </v-container>
    </main>
</template>

<style>
    main > .container {
    height: 100vh;
    }
</style>


<script>
//Components
import snackbar from '../components/Snackbar.vue'

//Plugins
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
            patternURL: require('../assets/ahoy.jpg'),

            genderList: [
              {text: "Male"},
              {text: "Female"}
            ],

            snackbar: { 
                text: "",
                timeout: 3000,
                flag: false
            }
        }
    },

    methods: { 
        register() {
            axios.post(`${process.env.API_URL}/user/`, {
                username: this.username,
                password: this.password,
                first_name: this.first_name,
                last_name: this.last_name,
                gender: this.gender.text
            })

            .then((res) => { 
              if(res.data.return == "Account successfully created.") { 
                this.snackbar.text = res.data.return

                axios.post(`${process.env.API_URL}/login/`, { 
                    username: this.username,
                    password: this.password
                })

                .then((res) => { 
                    if(res.data.pk > 0) { 
                        const user = {
                        username: res.data.username,
                        userID: res.data.pk,
                        profilePic: process.env.API_URL + res.data.profile_picture,
                        fullName: res.data.first_name + " " + res.data.last_name, 
                        config: { 
                            headers: {
                                Authorization: `Token ${res.data.token}`
                            }
                        }
                    }

                    this.snackbar = { 
                        text: "Welcome back",
                        flag: true
                    }

                    localStorage.setItem("token", res.data.token)
                    this.$store.dispatch("setUserData", user)
                    window.location.replace("/")
                    }
                })
              }
            })

            .catch((err) => { 
                this.snackbar.text = "Something went wrong."
                this.snackbar.flag = true
            })
        }
    },

    components: { 
        snackbar
    }
}
</script>
