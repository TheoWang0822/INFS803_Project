<template>
  <div class="weather-app">
    <!-- favorite cities -->
    <main class="content">
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
import { defineComponent } from "vue";
import weatherDao from "@/dao/weatherDao"; // key : get data via Dao
////////////////////////////////////////////////////////////
import { ref, onMounted } from "vue";
import { getCurrentTime } from "@/dao/weatherDao";

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
    onMounted(async () => {
      favorites.value = await weatherDao.getFavorites();
    });
    return {
      favorites,
      hotCities,
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

.grid-container {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin-top: 20px;
}

.weather-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s;
}

.weather-card:hover {
  transform: translateY(-3px); /* hover */
}

/* font */
.city-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.temp {
  font-size: 1.8rem;
  font-weight: bold;
  color: #42b983;
}

.high-low {
  color: #666;
  margin-top: 8px;
  font-size: 0.9rem;
}

.nav-bar {
}

.content h1 {
  text-align: left;
  margin-left: 0;
  margin-top: 30px;
  padding-left: 0;
  font-size: 1.8rem;
  color: #2c3e50;
  border-bottom: 2px solid #42b983;
  padding-bottom: 0.5rem;
}
</style>
