<template>
  <nav>
    <!--    <router-link to="/">Home</router-link> |
    <router-link to="/about">About</router-link>-->
    <NavBar show-back-button />
  </nav>
  <router-view />
</template>

<script lang="ts">
import { defineComponent } from "vue";
import NavBar from "@/components/NavBar.vue";

export default defineComponent({
  components: { NavBar },
});
</script>

<style>
html,
body,
#app {
  background: linear-gradient(135deg, #1b2735 0%, #090a0f 100%);
  height: 100%;
  margin: 0;
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}
</style>
