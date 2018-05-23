<template>
  <div class="container" >
    <p class="is-size-5">Categories</p> 
    <div class="columns is-multiline is-1">

      <div class="column is-2-desktop" v-for="(item, index) in categories" :key="`item-${index}`">
        <div :href="item.link" class="card" :style="{backgroundColor: item.color}">
          <header class="card-header">
            <!-- <p class="card-header-title">
              Component
            </p> -->
            <!-- <a href="#" class="card-header-icon" aria-label="more options">
              <span class="icon">
                <i class="fas fa-angle-down" aria-hidden="true"></i>
              </span>
            </a> -->
          </header>
          <div class="card-content">
            <div class="content has-text-centered">
              <i class="is-size-1 material-icons">school</i>
            </div>
          </div>
          <footer class="card-footer">
            <p class="card-footer-item">{{ item.name }}</p>
            <!-- <a href="#" class="card-footer-item">Save</a>
            <a href="#" class="card-footer-item">Edit</a>
            <a href="#" class="card-footer-item">Delete</a> -->
          </footer>
        </div>
      </div>
    </div>

    <p class="is-size-5"  style="margin-top: 5vh;">Most Recent Appeals</p> 
    <div class="columns">
      <div class="column">
        <p v-for="(item, index) in appeals" :key="`item-${index}`">
          {{ item.name }} needs help with {{ item.school }} {{ item.time }} ago
        </p>
        
      </div>
    
    </div>
    
  </div>
</template>

<script>
export default {
  data() { 
    return { 
      categories: [
        {name: "School", link: "/appeal/category/school", color: "#black"},
        {name: "Work", link: "/appeal/category/work", color: "#black"},
        {name: "Relationships", link: "/appeal/category/relationships", color: "#black"},
        {name: "Family", link: "/appeal/category/family", color: "#black"},
        {name: "School", link: "/appeal/category/school", color: "#black"},
        {name: "Work", link: "/appeal/category/work", color: "#black"},
        {name: "Relationships", link: "/appeal/category/relationships", color: "#black"},
        {name: "Family", link: "/appeal/category/family", color: "#black"},
        {name: "School", link: "/appeal/category/school", color: "#black"},
        {name: "Work", link: "/appeal/category/work", color: "#black"},
        {name: "Relationships", link: "/appeal/category/relationships", color: "#black"},
        {name: "Family", link: "/appeal/category/family", color: "#black"},
      ],

      appeals: [
        {name: "Mike Hawk", category: "School", time: "10s"},
        {name: "Mike Hawk", category: "School", time: "10s"},
        {name: "Mike Hawk", category: "School", time: "10s"},
        {name: "Mike Hawk", category: "School", time: "10s"},
        {name: "Mike Hawk", category: "School", time: "10s"},
        {name: "Mike Hawk", category: "School", time: "10s"},
        {name: "Mike Hawk", category: "School", time: "10s"},
        {name: "Mike Hawk", category: "School", time: "10s"},
        {name: "Mike Hawk", category: "School", time: "10s"},
      ]
    }
  }
}
</script>
