<template>
    <div>
        <v-toolbar flat>
            <v-toolbar-side-icon @click="drawer = !drawer"></v-toolbar-side-icon>
            <v-toolbar-title>
                <h1>A<span class="red--text">LIVE</span></h1>
            </v-toolbar-title>
            <v-spacer></v-spacer>
        
            <v-spacer></v-spacer>
            <v-select
                :items="items"
                v-model="searchText"
                item-text="request_title"

                @keyup="updateResults"
                prepend-icon="search"
                autocomplete
                label="Search"
                solo
                class="mx-3"
                flat
                align-center
            ></v-select>

                <v-btn icon to="/appeal/create">
                    <v-avatar>
                        <v-icon>add</v-icon>
                    </v-avatar>
                </v-btn>
                

            <v-toolbar-items class="hidden-sm-and-down">          
                <v-btn
                    color="red"
                    flat 
                    v-show="!isLoggedIn"
                    to="/login"
                    >
                    Sign in
                </v-btn>
                
            </v-toolbar-items>        

            <v-menu origin="top right" transition="scale-transition" bottom left offset-y v-show="isLoggedIn">
                <v-btn icon slot="activator">
                    <v-badge overlap>
                        <span slot="badge" class="caption" v-if="numOfNewNotifications > 0">{{ numOfNewNotifications }}</span>
                        <v-icon>notifications</v-icon>
                    </v-badge>               
                </v-btn>

                <v-list>
                    <v-list-tile v-for="(item, index) in notifications" :key="`item-${index}`" :to="item.link">
                        <v-list-tile-title class="body-1"> {{item.message}}</v-list-tile-title>
                    </v-list-tile>
                </v-list>
            </v-menu>

            <v-menu
                origin="top right"
                transition="scale-transition"
                :nudge-width="180"
                v-model="menu"
                bottom
                right
                offset-y
                v-show="isLoggedIn"
                >
                <v-btn icon slot="activator">
                    <span slot="badge" class="caption">3</span>
                    <v-avatar size="32px">
                        <img :src="`${userData.profilePic}`">
                    </v-avatar>             
                </v-btn>  
                <v-card>
                    <v-list>
                    <v-list-tile avatar>
                        <v-list-tile-avatar>
                        <img :src="`${userData.profilePic}`" alt="John">
                        </v-list-tile-avatar>
                        <v-list-tile-content>
                        <v-list-tile-title>{{ userData.fullName }}</v-list-tile-title>
                        <v-list-tile-sub-title> @{{ userData.username }} </v-list-tile-sub-title>
                        </v-list-tile-content>
                    </v-list-tile>
                    </v-list>
                    <v-divider></v-divider>
                    <v-list>
                        <v-list-tile :to="`/profile/${userData.userID}`">
                            <v-list-tile-action>
                                <v-icon size="20">fas fa-user-circle</v-icon>
                            </v-list-tile-action>
                            
                            <v-list-tile-title class="body-1">Profile</v-list-tile-title>
                        </v-list-tile>
                        <v-list-tile to="/settings">
                            <v-list-tile-action>
                                <v-icon size="20">fas fa-cog</v-icon>
                            </v-list-tile-action>
                            
                            <v-list-tile-title class="body-1">Settings</v-list-tile-title>
                        </v-list-tile>                    
                        <v-list-tile to="/logout">
                            <v-list-tile-action>
                                <v-icon size="20">fas fa-sign-out-alt</v-icon>
                            </v-list-tile-action>
                            
                            <v-list-tile-title class="body-1">Logout</v-list-tile-title>
                        </v-list-tile>
                    </v-list>
                </v-card>
            </v-menu>        
        </v-toolbar>

        <v-navigation-drawer
        v-model="drawer"
        temporary
        absolute
        >
        <v-toolbar flat>
        <v-list>
            <v-list-tile>
            <v-list-tile-title class="title">
                Navigation
            </v-list-tile-title>
            </v-list-tile>
        </v-list>
        </v-toolbar>
        <v-divider></v-divider>
        <v-spacer></v-spacer>
        <v-list class="pa-1" dense>
            <v-list-tile tag="div" to="/">
            <v-list-tile-action>
                <v-list-tile-title>Home</v-list-tile-title>
            </v-list-tile-action>
            </v-list-tile>

            <v-list-tile avatar tag="div" to="/appeals">
            <v-list-tile-action>
                <v-list-tile-title>Appeals</v-list-tile-title>
            </v-list-tile-action>
            </v-list-tile>
        </v-list>
        </v-navigation-drawer>        

        {{ notifications }}
    </div>
    
</template>

<script>
import axios from 'axios'

export default {
    data() { 
        return { 
            drawer: false,

            notifications: [
                
            ],


            fav: true,
            menu: false,
            message: false,
            hints: true,
            fullName: "John Doe",
            searchText: "",

            items: [],
        }
    },

    methods: { 
        updateResults() { 
            axios.get(`${process.env.API_URL}/search?search=${this.searchText}`, this.$store.getters.getConfig)
            .then((res) => { 
                this.items = res.data
            })
        },

        notifyMe() {

        }
    },
    
    computed: { 
        isLoggedIn() { 
            return ( (this.$store.getters.getUsername.length == 0) ? false: true)
        },

        username() { 
            return this.$store.getters.getUsername
        },

        userID() { 
            return this.$store.getters.getUserID
        },

        userData() { 
            return this.$store.getters.getUserData
        }, 

        numOfNewNotifications() { 
            let ctr = 0;

            for(let i = 0; i < this.notifications.length; i++) { 
                if(!this.notifications[i].seen) { 
                    ctr++
                }
            }

            return ctr
        }
    },

    watch: { 

    },

    created() { 
        setInterval(function() { 
            axios.get(`${process.env.API_URL}/notification/`, this.$store.getters.getConfig)
            .then((res) => { 
                this.notifications = res.data
            })
        }.bind(this), 1000)
    },
}
</script>