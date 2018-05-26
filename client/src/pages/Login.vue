<template>
    <v-container>
        <v-layout row justify-center> 
            <v-flex xs8 sm6 md5 lg4 xl4 mt-5 pa-2>
                <v-card class="pa-4" tile>
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
                        <v-btn color="success" @click="login()">Login</v-btn>
                    </v-form>
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
        
</template>

<script>
import axios from 'axios'

export default {
    data() { 
        return { 
            username: "",
            password: "",
            seePass: false,

            snackbarMessage: "",
            snackbar: false,
        }
    },

    methods: { 
        login() {
            axios.post("http://192.168.1.2:8000/login/", {
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

        console.log(process.env.baseUrl)
    }
}
</script>
