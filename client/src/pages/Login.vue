<template>
    <main :style="`background-image: url(${patternURL}); background-repeat: repeat;`">
        <v-container fill-height>
            <v-layout align-center justify-center> 
                <v-flex xs10 sm8 md7 lg4 xl3>
                    <v-card class="pa-4 elevation-10">
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
                                <v-btn color="primary" @click="login()" large>Login</v-btn>
                                <router-link to="/register">Create an account</router-link>
                        </v-card-text>
                        
                    </v-card>
                </v-flex>

                <v-snackbar
                    v-model="snackbar"
                    bottom
                    right>

                    {{ snackbarMessage }}
                    <v-btn flat color="white" @click.native="snackbar = false">Close</v-btn>
                </v-snackbar>            
            </v-layout>
        </v-container>
    </main>
</template>

<script>
import axios from 'axios'
import sun from '../components/Sun.vue'
import anime from 'animejs'

export default {
    data() { 
        return { 
            username: "",
            password: "",
            seePass: false,

            snackbarMessage: "",
            snackbar: false,
            patternURL: require('../assets/science.png'),
        }
    },

    methods: { 
        login() {
            console.log(`${process.env.API_URL}`)
            axios.post(`${process.env.API_URL}/login`, {
                username: this.username,
                password: this.password
            })

            .then((res) => { 
                if(res.data.user > 0) { 
                    localStorage.setItem("token", res.data.token)
                    this.$store.commit("setUsername", this.username)
                    this.$router.push("/")
                }

                
            })

            .catch((err) => { 
                this.snackbarMessage = "Invalid login."
                this.snackbar = true
            })
        }
    },

    beforeCreate() { 
        if(localStorage.getItem("token") != null) { 
            this.$router.push("/")
        }

        console.log(process.env)
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
        sun
    }
}
</script>

<style>
    main > .container {
    height: 100vh;
    }
</style>
