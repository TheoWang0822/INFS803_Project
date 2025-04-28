<template>
  <div class="weather-card">
    <h2>{{ city }}</h2>
    <div class="weather-main">
      <div class="temp">{{ temperature }}°C</div>
    </div>
    <p class="description">{{ description }}</p>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
  name: "WeatherCard",
  props: {
    city: {
      type: String,
      required: true,
    },
    temperature: {
      type: Number,
      required: true,
    },
    description: {
      type: String,
      required: true,
    },
    iconCode: {
      type: String,
      required: true,
    },
  },
  /*computed: {
    iconUrl(): string {
      return `https://openweathermap.org/img/wn/${this.iconCode}@2x.png`;
    },
  },*/
});
</script>

<style scoped>
.weather-card {
  width: 240px;
  padding: 16px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  background-color: #f1f5f9;
  text-align: center;
  transition: 0.3s ease;
}
.weather-card:hover {
  transform: scale(1.03);
}
.weather-main {
  display: flex;
  align-items: center;
  justify-content: center;
}
.weather-main img {
  width: 60px;
  height: 60px;
}
.temp {
  font-size: 32px;
  font-weight: bold;
  margin-left: 12px;
}
.description {
  color: #555;
  margin-top: 8px;
  text-transform: capitalize;
}
</style>
