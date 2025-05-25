<template>
  <div class="weather-app">
    <!-- favorite cities -->
    <main class="content">
      <div v-if="!userInfo">
        <h1>Your favorites</h1>
        <div class="grid-container">
          <div
            v-for="(city, index) in favorites"
            :key="index"
            class="weather-card"
          >
            <div class="city-header">
              <h2>{{ city.city }}</h2>
              <span class="temp">{{ city.temp }}</span>
            </div>
            <div class="condition">{{ city.condition }}</div>
            <div class="high-low">H:{{ city.high }} L:{{ city.low }}</div>
          </div>
        </div>
      </div>

      <!-- hot cities -->
      <section style="margin-top: 40px">
        <h1>Hot cities</h1>
        <div class="grid-container">
          <div
            v-for="(city, index) in hotCities"
            :key="'hot-' + index"
            class="weather-card"
          >
            <div class="city-header">
              <h2>{{ city.city }}</h2>
              <span class="temp">{{ city.temp }}</span>
            </div>
            <div class="condition">{{ city.condition }}</div>
            <div class="high-low">H:{{ city.high }} L:{{ city.low }}</div>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script lang="ts">
import { defineComponent, onBeforeUnmount } from "vue";
import weatherDao from "@/dao/weatherDao"; // key : get data via Dao
////////////////////////////////////////////////////////////
import { ref, onMounted } from "vue";
import { getAllHotCityInfo } from "@/dao/weatherDao";
import { GetUserInfo } from "@/dao/userDao";

/////////////////////////////////////////////////////

interface WeatherData {
  city: string;
  temp: string;
  condition: string;
  high: string;
  low: string;
}

export default defineComponent({
  setup() {
    const favorites = ref<WeatherData[]>([]);
    const hotCities = ref<WeatherData[]>([]);
    const hotCityList = ref<any>(null);
    const userInfo = ref<null | { username: string }>(null);
    onMounted(async () => {
      favorites.value = await weatherDao.getFavorites();
      hotCityList.value = await getAllHotCityInfo();
      console.log("热门城市: ", hotCityList.value);
      checkIsLoggedIn();
      window.addEventListener("user-logged-in", checkIsLoggedIn);
      window.addEventListener("user-logged-out", checkIsLoggedIn);
    });
    onBeforeUnmount(() => {
      window.removeEventListener("user-logged-in", checkIsLoggedIn);
      window.removeEventListener("user-logged-out", checkIsLoggedIn);
    });
    async function checkIsLoggedIn() {
      try {
        userInfo.value = await GetUserInfo();
        if (userInfo.value != null) {
          //console.log("这是测试数据1: ", userInfo.value);
        } else {
          //console.log("这是测试数据2: ", userInfo.value);
        }
      } catch {
        userInfo.value = null;
      }
    }
    return {
      favorites,
      hotCities,
      userInfo,
    };
  },
});
</script>

<style scoped>
.city-card {
  padding: 1rem;
  margin: 1rem 0;
  border: 1px solid #ddd;
  border-radius: 8px;
}

.weather-card {
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.18);
  border-radius: 16px;
  padding: 20px;
  backdrop-filter: blur(10px);
  box-shadow: 0 4px 20px rgba(0, 255, 255, 0.15);
  color: #ffffff;
  transition: transform 0.3s, box-shadow 0.3s;
}

.weather-card:hover {
  transform: scale(1.03);
  box-shadow: 0 8px 28px rgba(0, 255, 255, 0.25);
}

.grid-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 24px;
  margin-top: 24px;
}

.city-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.temp {
  font-size: 2rem;
  font-weight: bold;
  color: #00ffe1;
  text-shadow: 0 0 6px #00ffe1;
}

.high-low {
  color: #ccc;
  margin-top: 10px;
  font-size: 1rem;
  font-weight: 300;
}

.content h1 {
  text-align: left;
  margin-top: 40px;
  font-size: 2rem;
  color: #00ffe1;
  border-bottom: 2px solid #00ffe1;
  padding-bottom: 8px;
  text-shadow: 0 0 4px #00ffe1;
}

.weather-app {
  background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
  min-height: 100vh;
  padding: 40px;
}
</style>
