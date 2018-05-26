<template>
    <v-toolbar flat dark prominent>
        <v-toolbar-title>
            Alive
        </v-toolbar-title>
    
        <v-spacer></v-spacer>

        <!-- <v-text-field
            prepend-icon="search"
            append-icon="mic"
            label="Search"
            solo-inverted
            class="mx-3"
            flat
            align-center
        ></v-text-field> -->

        <v-toolbar-items class="hidden-sm-and-down">          
            <v-btn 
                flat 
                to="/"
                >
                Home
            </v-btn>
            <v-btn 
                flat 
                to="/appeal"
                >
                Appeal
            </v-btn>
            <v-btn 
                flat 
                v-show="!isLoggedIn"
                to="/login"
                >
                Sign in
            </v-btn>
            
        </v-toolbar-items>        

        <v-menu
        origin="top right"
        transition="scale-transition"
        bottom 
        left
        offset-y
        dark
        v-show="isLoggedIn"
        >
            <v-btn icon slot="activator">
                <v-badge overlap>
                    <span slot="badge" class="caption">3</span>
                    <!-- <v-avatar size="32px">
                        <img src="https://randomuser.me/api/portraits/men/1.jpg">
                    </v-avatar> -->
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
            dark
            v-show="isLoggedIn"
            >
            <v-btn icon slot="activator">
                <span slot="badge" class="caption">3</span>
                <v-avatar size="32px">
                    <img src="https://randomuser.me/api/portraits/men/1.jpg">
                </v-avatar>             
            </v-btn>  
            <v-card>
                <v-list>
                <v-list-tile avatar>
                    <v-list-tile-avatar>
                    <img src="https://vuetifyjs.com/static/doc-images/john.jpg" alt="John">
                    </v-list-tile-avatar>
                    <v-list-tile-content>
                    <v-list-tile-title>{{ fullName }}</v-list-tile-title>
                    <v-list-tile-sub-title> @{{ username }} </v-list-tile-sub-title>
                    </v-list-tile-content>
                    <!-- <v-list-tile-action>
                        
                            <v-btn
                                :class="fav ? 'yellow--text' : ''"
                                icon
                                @click="fav = !fav"
                            >
                                <v-icon>fas fa-star</v-icon>
                            </v-btn>
                            
                        
                    
                    </v-list-tile-action> -->
                </v-list-tile>
                </v-list>
                <v-divider></v-divider>
                <v-list>
                    <v-list-tile :to="`/profile/${username}`">
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
                <!-- <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn flat @click="menu = false">Cancel</v-btn>
                <v-btn color="primary" flat @click="menu = false">Save</v-btn>
                </v-card-actions> -->
            </v-card>
        </v-menu>        
    </v-toolbar>
</template>

<script>
export default {
    data() { 
        return { 
            avatarMenu: [
                {name: "Profile", link: ``, clickable: true, icon: "fas fa-user-circle"},
                {name: "Settings", link: `/settings`, clickable: true, icon: "fas fa-cog"},
                {name: "Logout", link: "/logout", icon: "fas fa-sign-out-alt"},
            ],

            notifications: [
                {message: "You received a request from LOMAO"}
            ],


            fav: true,
            menu: false,
            message: false,
            hints: true,
            fullName: "John Doe"
        }
    },

    created() {
        
    },
    
    computed: { 
        isLoggedIn() { 
            return ( (this.$store.getters.getUsername.length == 0) ? false: true)
        },

        username() { 
            return this.$store.getters.getUsername
        }
    }
}
</script>

<style>
    .pl-10 { 
        padding-left: 160px
    }

    .pr-10 { 
        padding-right: 160px
    }
</style>

