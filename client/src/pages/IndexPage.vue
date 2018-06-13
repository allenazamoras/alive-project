<template>
  <div>
    <v-container>
      <!-- <v-dialog v-model="dialog" max-width="290" persistent>
        <v-card>
          <v-card-title class="headline">How was the session?</v-card-title>
          <v-card-text>
          <v-text-field placeholder="rating number"></v-text-field>
          <v-text-field placeholder="Describe what you thought." multi-line></v-text-field>
          <v-btn color="green darken-1" outline round dark block @click="">Rate</v-btn>
          </v-card-text>
        </v-card>
      </v-dialog> -->
    </v-container>
  </div>
</template>

<script>
import {mapState} from 'vuex'

export default {
  data() { 
    return { 
      dialog: true
    }
  }
}
</script>
