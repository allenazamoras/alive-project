<template>
  <div>
    <app-nav></app-nav>
    <v-container grid-list-lg>
      <v-layout  justify-center align-center>
        <v-flex xs12 sm12 md12 lg12 xl12>
        <v-card tile>
          <v-card-media src="" height="300" class="" style="background-image: url('http://192.168.1.131:8000/src/assets/sun-pattern.png'); background-repeat: repeat;">
            <v-layout row justify-center align-center>
              <v-flex md12 lg12 sm12 class="text-sm-center">
                <v-avatar size="110">
                  <img src="https://randomuser.me/api/portraits/men/1.jpg" alt="">
                </v-avatar>

                <h2 class="grey--text text--darken-3">John Doe</h2>
                <router-link to="/"><h4 class="body-1 grey--text text--darken-3">@johndoe</h4></router-link>
                <h4 class="body-1 grey--text text--darken-3">Programmer | Depressed 🅱OI | Knee Gore</h4>
              </v-flex>          
            </v-layout>
          </v-card-media>        
        </v-card>
        </v-flex>
      </v-layout>

      <v-layout row grid-list-lg>
        <v-flex lg4>
          <v-card tile height="100">
            <!-- <v-card-media src="" height="100" class="">
              <v-layout row justify-center align-center>
                <v-flex lg4>
                  <h1>Panic Attacks: 100</h1>
                </v-flex>          
              </v-layout>
            </v-card-media> -->

            <v-card-title>
              <h1>Panic Attacks: 100</h1>
            </v-card-title>
          </v-card>  
        </v-flex>

        <v-flex lg4>
          <v-card tile>
            <v-card-media src="" height="100" class="">
              <v-layout row justify-center align-center>
                <v-flex lg4 class="text-sm-center">
                  
                </v-flex>          
              </v-layout>
            </v-card-media>
          </v-card>  
        </v-flex>

        <v-flex lg4>
          <v-card tile>
            <v-card-media src="" height="100" class="">
              <v-layout row justify-center align-center>
                <v-flex lg4 class="text-sm-center">
                  
                </v-flex>          
              </v-layout>
            </v-card-media>
          </v-card>  
        </v-flex>        
      </v-layout>
    </v-container>
  </div>
  
</template>

<script>
import appNav from '../.././components/AppNav.vue'

export default {
  data() { 
    return { 
    }
  },

  computed: { 
    username() { 
      return this.$store.getters.getUsername
    }
  },

  components: { 
    appNav
  },

  created() { 
    this.username = this.$route.params
  }
}
</script>