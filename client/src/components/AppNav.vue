<template>
    <v-toolbar dark mb-4 dense>
        <v-toolbar-title>
            Alive
        </v-toolbar-title>

        <v-spacer></v-spacer>

        <v-toolbar-items class="hidden-sm-and-down">
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

        <v-toolbar-side-icon class="hidden-md-and-up">

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

