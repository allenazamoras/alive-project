<template>
        <v-layout>
            <v-flex xs8 sm6 md4 offset-md4 mt-5>
                <v-card class="pa-5" round>
                    <v-form>
                        <v-text-field
                            label="Username"
                            v-model="username"
                            required
                        ></v-text-field>
                        <v-text-field
                            label="Password"
                            v-model="password"
                            :append-icon="seePass ? 'visibility_off' : 'visibility'"
                            :append-icon-cb="() => (seePass = !seePass)"
                            :type="seePass ? 'text' : 'password'"
                            required
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
        login: () => { 
            axios.post("url", {
                username: this.username,
                password: this.password
            })

            .then((res) => { 
                console.log(res)
            })
        }
    }
}
</script>
