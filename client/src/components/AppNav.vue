<template>
    <div>
        <v-toolbar class="elevation-0">
        <v-toolbar-side-icon @click="drawer = !drawer"></v-toolbar-side-icon>
        <v-toolbar-title>
            <h1>A<span class="red--text">LIVE</span></h1>
        </v-toolbar-title>
        <v-spacer></v-spacer>
    
        <v-spacer></v-spacer>

        <v-btn icon to="/search">
            <v-avatar>
                <v-icon>search</v-icon>
            </v-avatar>
        </v-btn>

        <v-btn icon to="/appeal/create" v-if="isLoggedIn">
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
                <v-list-tile v-for="(item, index) in notifications" :key="`item-${index}`" :to="item.link" v-if="notifications.length > 0">
                    <v-list-tile-title class="body-1"> {{item.message}}</v-list-tile-title>
                </v-list-tile>
                <v-list-tile v-if="notifications.length == 0">
                    <span class="grey--text body-1">
                        No new notifications.
                    </span>
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
            v-if="isLoggedIn"
            >
            <v-btn icon slot="activator">
                <span slot="badge" class="caption">3</span>
                <v-avatar size="32px">
                    <img :src="`${getUserData.profilePic}`">
                </v-avatar>             
            </v-btn>  
            <v-card>
                <v-list>
                <v-list-tile avatar>
                    <v-list-tile-avatar>
                    <img :src="`${getUserData.profilePic}`" alt="John">
                    </v-list-tile-avatar>
                    <v-list-tile-content>
                    <v-list-tile-title>{{ getUserData.fullName }}</v-list-tile-title>
                    <v-list-tile-sub-title> @{{ getUserData.username }} </v-list-tile-sub-title>
                    </v-list-tile-content>
                </v-list-tile>
                </v-list>
                <v-divider></v-divider>
                <v-list>
                    <v-list-tile :to="`/profile/${getUserData.userID}`">
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
    
    <v-dialog v-model="userDialog" max-width="290" persistent>
      <v-card>
        <v-card-title class="headline">{{request[0].helper.first_name}} {{ request[0].helper.last_name }}</v-card-title>
        <v-card-text>
          is requesting to help you
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="green darken-1" flat="flat" @click.native="accept">Accept</v-btn>
          <v-btn color="green darken-1" flat="flat" @click.native="flag = false">Decline</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    {{getConfig}}

    {{request}}
    </div>
</template>

<script>
import axios from 'axios'
import {mapGetters, mapState} from 'vuex'

export default {
    data() { 
        return { 
            drawer: false,

            flag: false,
            notifications: [],
            request: [],

            fav: true,
            menu: false,
            message: false,
            hints: true,
            searchText: "",
        }
    },

    methods: {
        getNotifications() { 
            axios.get(`${process.env.API_URL}/notification/`, this.getConfig)
            .then((res) => { 
                this.notifications = res.data.notification
                this.request = res.data.request
                console.log(res)
                setTimeout(this.getNotifications, 1500)
            })
        },

        accept() { 
            axios.post(`${process.env.API_URL}/pending/${request[0].id}/`, {
                
            })
        }
    },

    created() { 
        this.getNotifications()
    },
    
    computed: { 
        userDialog: { 
            set() { 
            },

            get() { 
                return this.request.length > 0 ? true: false
            },
        },

        numOfNewNotifications() { 
            let ctr = 0;

            for(let i = 0; i < this.notifications.length; i++) { 
                if(!this.notifications[i].seen) { 
                    ctr++
                }
            }

            return ctr
        },

        ...mapGetters('userModule', [
            'isLoggedIn', 'getUserData', 'getConfig'
        ]),

        ...mapState('sessionModule', [
            'appealID'
        ])
    }
}
</script>