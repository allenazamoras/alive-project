<template>
    <v-toolbar mb-4 dense>
        <!-- <v-spacer></v-spacer> -->
        <v-toolbar-items class="hidden-xs">
            <v-btn 
                flat 
                v-for="(item, index) in routes" 
                :key="`item-${index}`"
                :to="item.link"
                v-show="item.show"
                >
                {{ item.name }}
            </v-btn>
            
        </v-toolbar-items>

        <v-toolbar-side-icon class="hidden-sm-and-up">

        </v-toolbar-side-icon>
    </v-toolbar>
</template>

<script>
export default {
    data() { 
        return { 
            routes: [
                {name: "home", link: "/", icon: true, show: true},
                {name: "appeal", link: "/appeal", icon: true, show: true},
                {name: "login", link: "/login", icon: false, show: (localStorage.getItem("token") != null) ? false: true},
                {name: "Register", link: "/register", icon: false, show: (localStorage.getItem("token") != null) ? false: true},
                {name: "logout", link: "/logout", icon: false, show: (localStorage.getItem("token") == null) ? false: true},
            ],

            avatarMenu: [
                {name: "Profile", link: `/profile/${this.$store.getters.getUsername}`, clickable: true}
            ],

            notifications: [
                {message: "You received a request from LOMAO"}
            ]
        }
    },

    created() {
        console.log(this.routes)
    }
}
</script>

<style>

</style>

