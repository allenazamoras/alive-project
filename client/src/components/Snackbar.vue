<template>
    <div>
        <v-snackbar
        v-model="snackbar.flag"
        :timeout="timeout"
        bottom left
        >
      {{ snackbar.text }}
    </v-snackbar>
    </div>
</template>

<script>
export default {
    data() { 
        return { 
            timeout: 3000
        }
    },

    props: { 
        snackbar: { 
            type: Object,

            default: function() { 
                return {
                    text: "",
                    flag: false
                }
            }
        }
    }
}
</script>
