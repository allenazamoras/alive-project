<template>
  <div>
    <div class="columns is-centered has-text-centered">
      <div class="column is-3-desktop is-8-mobile is-offset-2-mobile is-8-tablet">   
        <p class="is-size-3 has-text-weight-bold">
          Login
        </p>     
        <register-logo/>
        <div class="field" style="margin-top: 5vh;">
          <!-- <label class="label">Username</label> -->
          <div class="control">
            <input class="input is-medium" type="text" placeholder="Username" v-model="username">
          </div>
          <!-- <p class="help">This is a help text</p> -->
        </div>
        <div class="field">
          <!-- <label class="label">Password</label> -->
          <div class="control">
            <input class="input is-medium" type="password" placeholder="Password" v-model="password">
          </div>
        </div>
        <button class="button is-success" style="width: 100%;" @click="login()">
          Login
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import registerLogo from '~/components/RegisterLogo.vue'
import axios from 'axios'

export default {
  data() { 
    return { 
      username: "",
      password: ""
    }
  },

  methods: { 
    login() { 
      axios.post("http://192.168.1.2:8000/login", { 
        username: this.username,
        password: this.password
      })
      .then( (res) => { 
        console.log(res)
      })
    }
  },
  components: {
    registerLogo
  }
}
</script>
