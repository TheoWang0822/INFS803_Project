<template>
  <div class="home">
    <img alt="Vue logo" src="../assets/logo.png" />
    <HelloWorld msg="Welcome to Your Vue.js + TypeScript App" />
    <!-- TODO : JUST FOR TESTING, WILL DELETE -->
    <button @click="goToWeatherPage" class="weather-button">
      Check the Weather Now 🌤️
    </button>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import HelloWorld from "@/components/HelloWorld.vue"; // @ is an alias to /src
import { useRouter } from "vue-router";

export default defineComponent({
  name: "HomeView",
  components: {
    HelloWorld,
  },
  setup() {
    const router = useRouter();

    // jump to weather page
    const goToWeatherPage = () => {
      router.push("/weather");
    };

    return {
      goToWeatherPage,
    };
  },
});
</script>
