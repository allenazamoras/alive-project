<template>
    <main 
        :style="`background-image: url(${patternURL}); background-repeat: repeat;`">
        <v-container 
            fill-height 
            grid-list-lg
        >
            <v-layout 
                align-center 
                justify-center
            > 
                <v-flex 
                    xs10 
                    sm8 
                    md7 
                    lg4 
                    xl3
                >
                    <v-card 
                        class="pa-3 elevation-10"
                    >
                        <v-card-text 
                            class="headline text-xs-center"
                        >
                            Register
                        </v-card-text>
                        <v-form 
                            class="pa-4 pb-5"
                            ref="form"
                        >
                            <v-text-field
                                label="Username"
                                v-model="username"
                                :rules="usernameRules"
                            ></v-text-field>
                            <v-text-field
                                label="Password"
                                v-model="password"
                                :rules="passwordRules"
                                :append-icon="seePass ? 'visibility_off' : 'visibility'"
                                :append-icon-cb="() => (seePass = !seePass)"
                                :type="seePass ? 'text' : 'password'"
                            
                            ></v-text-field>

                            <v-layout>
                                <v-flex xs12 sm12 md6>
                                <v-text-field
                                    label="First Name"
                                    :rules="firstNameRules"
                                    v-model="first_name"
                                ></v-text-field>
                                </v-flex>

                                <v-flex xs12 sm12 md6>
                                <v-text-field
                                    label="Last Name"
                                    :rules="lastNameRules"
                                    v-model="last_name"
                                ></v-text-field>
                                </v-flex>
                                
                            </v-layout>
                            <v-select
                                v-model="gender"
                                :items="genderList"
                                :rules="genderRules"
                                label="Gender"
                                single-line>
                            </v-select>
                        </v-form>
                        <v-card-text 
                            flex
                        >
                            <v-btn 
                                color="primary" 
                                @click="register" 
                                large
                            >Register</v-btn>
                            <router-link 
                                to="/login"
                            >Sign in instead</router-link>
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
import {mapActions} from 'vuex'

export default {
    data() { 
        return { 
            username: "",
            usernameRules: [
                v => !!v || 'Username is required',
            ],
            password: "",
            passwordRules: [
                v => !!v || 'Password is required',
                v => (v && v.length > 6) || 'Password must be more than 6 characters.'
            ],
            first_name: "",
            firstNameRules: [
                v => !!v || 'First name is required',
            ],
            last_name: "",
            lastNameRules: [
                v => !!v || 'Last name is required',
            ],
            gender: "",
            genderRules: [
                () => (this.gender == "") ? 'Gender is required': true
            ],
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
            if (this.$refs.form.validate()) {   
                axios.post(`${process.env.API_URL}/user/`, {
                    username: this.username,
                    password: this.password,
                    first_name: this.first_name,
                    last_name: this.last_name,
                    gender: this.gender.text
                })
                .then((res) => { 
                    if(res.data.return == "Account successfully created.") { 
                        this.$router.push('/login')
                    }
                    this.snackbar.text = res.data.return
                    this.snackbar.flag = true
                })
                .catch((err) => { 
                    console.log(err)
                    this.snackbar.text = "Something went wrong."
                    this.snackbar.flag = true
                })
            }
        },
        ...mapActions('userModule', [
            'setUserData'
        ])
    },
    components: { 
        snackbar
    }
}
</script>
