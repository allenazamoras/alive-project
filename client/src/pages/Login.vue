<template>
        <v-layout row justify-center> 
            <v-flex xs8 sm6 md3 xl4 mt-5 pa-2>
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
                        <v-btn color="success" @click="login()">Login</v-btn>
                    </v-form>
                </v-card>
            </v-flex>
        </v-layout>
</template>

<script>
import axios from 'axios'

export default {
    data() { 
        return { 
            username: "",
            password: "",
            seePass: false
        }
    },

    methods: { 
        login() {
            axios.post("http://192.168.1.2:8000/login/", {
                username: this.username,
                password: this.password
            })

            .then((res) => { 
                localStorage.setItem("token", res.data.token)
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
