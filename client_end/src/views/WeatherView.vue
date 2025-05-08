<template>
  <div class="weather-app">
    <!-- 收藏城市 -->
    <section>
      <h2>Your favorites</h2>
      <div v-for="city in favorites" :key="city.city" class="city-card">
        <h3>{{ city.city }}</h3>
        <p>{{ city.temp }} {{ city.condition }}</p>
        <small>H:{{ city.high }} L:{{ city.low }}</small>
      </div>
    </section>

    <!-- 热门城市 -->
    <section>
      <h2>Hot cities</h2>
      <div v-for="city in hotCities" :key="city.city" class="city-card">
        <h3>{{ city.city }}</h3>
        <p>{{ city.temp }} {{ city.condition }}</p>
        <small>H:{{ city.high }} L:{{ city.low }}</small>
      </div>
    </section>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import weatherDao from "@/dao/weatherDao"; // 关键点：通过DAO获取数据

interface WeatherData {
  city: string;
  temp: string;
  condition: string;
  high: string;
  low: string;
}

export default defineComponent({
  data() {
    return {
      favorites: [] as WeatherData[],
      hotCities: [] as WeatherData[],
    };
  },
  async created() {
    // 通过 DAO 获取数据
    this.favorites = await weatherDao.getFavorites();
    this.hotCities = await weatherDao.getHotCities();
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
</style>
