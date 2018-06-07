<template>
    <main :style="`background-image: url(${patternURL}); background-repeat: repeat;`">
        <v-container fill-height>
            <v-layout align-center justify-center> 
                <v-flex xs10 sm8 md7 lg4 xl3>
                    <v-card class="pa-4 elevation-10">
                        <v-card-text class="text-xs-center headline">
                            Login
                        </v-card-text>
                        <v-card-text class="text-xs-center">
                            <sun/>
                        </v-card-text>
                        
                        <v-card-text class="subheading text-xs-center grey--text text--darken-2" id="greeting" style="opacity: 0;">
                            We're glad you're here.
                        </v-card-text>
                        <v-form class="pa-4 pb-5">
                            <v-text-field
                                label="Username"
                                v-model="username"
                                color="red"
                            ></v-text-field>
                            <v-text-field
                                label="Password"
                                v-model="password"
                                :append-icon="seePass ? 'visibility_off' : 'visibility'"
                                :append-icon-cb="() => (seePass = !seePass)"
                                :type="seePass ? 'text' : 'password'"
                                color="red"
                            
                            ></v-text-field>
                        </v-form>
                        <v-card-text flex>
                            <v-btn color="primary" @click="login" large>Login</v-btn>
                            <router-link to="/register">Create an account</router-link>
                        </v-card-text>
                        
                    </v-card>
                </v-flex>
            </v-layout> 

            <snackbar :snackbar="snackbar"/>
        </v-container>
    </main>
</template>

<script>
//Components
import sun from '../components/Sun.vue'
import snackbar from '../components/Snackbar.vue'

//Plugins
import axios from 'axios'
import anime from 'animejs'
import {mapActions} from 'vuex'

export default {
    data() { 
        return { 
            username: "",
            password: "",

            seePass: false,
            patternURL: require('../assets/ahoy.jpg'),

            snackbar: {}
        }
    },

    methods: { 
        ...mapActions('userModule', [
            'setUserData'
        ]),
        
        login() {
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
                    this.setUserData(user)
                    window.location.replace("/")
                }
            })

            .catch((err) => { 
                this.snackbar = { 
                    text: err.response.data.non_field_errors[0],
                    flag: true
                }
                console.log(err)
            })
        }
    },

    mounted() { 
        anime({
            targets: '#greeting',
            easing: 'easeInOutQuad',
            duration: 1000,
            opacity: 1,
        });
    },

    components: { 
        sun,
        snackbar
    }
}
</script>

<style>
    main > .container {
        height: 100vh;
    }
</style>
