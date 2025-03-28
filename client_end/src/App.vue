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
import NavBar from "@/components/NavBar.vue"; // 引入组件

export default defineComponent({
  components: { NavBar },
});
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
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
