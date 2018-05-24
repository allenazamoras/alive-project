<template>
  <div>
    <nav class="navbar is-white is-shadowless" role="navigation" aria-label="main navigation">
      <div class="container">
        <div class="navbar-brand">
          <p class="navbar-item is-size-4">
            Alive
          </p>

          <a role="button" class="navbar-burger" aria-label="menu" aria-expanded="false">
            <span aria-hidden="true"></span>
            <span aria-hidden="true"></span>
            <span aria-hidden="true"></span>
          </a>
        </div>

        <div class="navbar-menu">
          <div class="navbar-start">
            <nuxt-link class="navbar-item" v-for="(item, index) in navStart" :key="`item-${index}`" :to="item.link">
              {{ item.title }}
            </nuxt-link>
            
          </div>
          <div class="navbar-end">
            <nuxt-link class="navbar-item" v-for="(item, index) in navEnd" :key="`item-${index}`" :to="item.link">
              {{ item.title }}
            </nuxt-link>
            
          </div>
        </div>
      </div>
    </nav>
  </div>
</template>

<script>
export default {
  data() { 
    return { 
      navStart: [
        {title: "Home", link: "/"},
        {title: "Appeal", link: "/appeal"}
      ],

      navEnd: [
        {title: "Login", link: "/login"},
        {title: "Register", link: "/register"},
      ]
    }
  }
}
</script>

