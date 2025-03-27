<template>
  <div class="home">
    <img alt="Vue logo" src="../assets/logo.png" />
    <HelloWorld msg="Welcome to Your Vue.js + TypeScript App" />
    <!-- 添加按钮 -->
    <button @click="goToWeatherPage" class="weather-button">
      Check the Weather Now 🌤️
    </button>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import HelloWorld from "@/components/HelloWorld.vue"; // @ is an alias to /src
import { useRouter } from "vue-router"; // 使用 Vue Router 的导航功能

export default defineComponent({
  name: "HomeView",
  components: {
    HelloWorld,
  },
  setup() {
    const router = useRouter();

    // 跳转到天气页面的方法
    const goToWeatherPage = () => {
      router.push("/weather"); // 或使用名称 router.push({ name: 'weather' })
    };

    return {
      goToWeatherPage,
    };
  },
});
</script>
