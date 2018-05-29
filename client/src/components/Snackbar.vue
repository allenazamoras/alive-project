<template>
    <div>
        <v-snackbar
        v-model="snackbar"
        :timeout="timeout"
        bottom left
        >
      {{ text }}
      <!-- <v-btn flat color="pink" @click.native="snackbar = false">Close</v-btn> -->
    </v-snackbar>
    </div>
</template>

<script>
export default {

    computed: { 
        snackbar: { 
            get: function() { 
                return this.$store.getters.getSnackbarState
            },

            set: function(flag) { 
                this.$store.commit("setSnackbarState", flag)
            }
            
        },

        timeout() { 
            return this.$store.getters.getSnackbarTimeout
        }
    },

    props: ['text']
}
</script>
