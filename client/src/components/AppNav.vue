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
                :to="item.link">
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
                {name: "home", link: "/", icon: true},
                {name: "login", link: "/login", icon: false},
                {name: "Register", link: "/register", icon: false},
            ]
        }
    }
}
</script>

<style>

</style>

