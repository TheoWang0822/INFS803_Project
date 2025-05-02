<!-- src/components/NavBar.vue -->
<template>
  <nav class="nav-bar">
    <img
      v-if="showBackButton"
      src="/images/weather-app.png"
      alt=""
      class="back-button"
      @click="goToHome"
    />
    <div class="nav-links">
      <router-link to="/">Home</router-link> |
      <router-link to="/about">About</router-link>
    </div>

    <div class="input-pos">
      <a-input-search
        v-model:value="searchValue"
        placeholder="input search text"
        style="width: 400px"
        @search="onSearch"
      />
    </div>
  </nav>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { useRouter } from "vue-router";
import { getCityInfo } from "@/dao/weatherDao";

import { ref } from "vue";

export default defineComponent({
  name: "NavBar",
  props: {
    showBackButton: {
      type: Boolean,
      default: false, // Default not display
    },
  },
  setup() {
    const router = useRouter();
    const searchValue = ref<string>("");
    const onSearch = async (value: string) => {
      const response = await getCityInfo(value);
      if (Object.keys(response).length !== 0) {
        router.push({
          name: "details",
          query: {
            id: response[0].id,
            cityname: response[0].cityname,
            country: response[0].country,
          },
        });
      } else {
        alert("No city found!");
      }
    };

    const goToHome = () => {
      searchValue.value = "";
      router.push("/");
    };

    return {
      goToHome,
      searchValue,
      onSearch,
    };
  },
});
</script>

<style scoped>
.nav-bar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 15px 20px;
  background: #f8f9fa;
  border-bottom: 1px solid #ddd;
  margin: 0;
  width: 100vw;
  box-sizing: border-box;
}

.back-button {
  width: 30px;
  height: 30px;
  cursor: pointer;
  transition: opacity 0.3s;
}

.back-button:hover {
  opacity: 0.7;
}

.nav-links {
  font-size: 1.2rem;
}

.nav-links a {
  color: #2c3e50;
  text-decoration: none;
}

.nav-links a.router-link-exact-active {
  color: #42b983;
}

.input-pos {
  flex: 10;
  display: flex;
  justify-content: center;
  padding-right: 150px;
}
</style>
