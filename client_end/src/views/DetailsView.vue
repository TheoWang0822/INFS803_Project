<script lang="ts">
import { useRoute } from "vue-router";
import { defineComponent, onMounted, ref, watch } from "vue";
import weatherDao, {
  getCityInfoById,
  getCityForecastInfoById,
} from "@/dao/weatherDao";
import { LoadingOutlined } from "@ant-design/icons-vue";

export default defineComponent({
  components: {
    LoadingOutlined,
  },
  setup() {
    const route = useRoute();
    const data = ref({});
    const allData = ref<any>(null);
    const currentDetail = ref<any>(null);
    const forecastDetail = ref<any>(null);
    const isLoaded = ref(false);
    const toEnglishDate = (dateString: string) => {
      const date = new Date(dateString);
      const day = date.getDate().toString().padStart(2, "0");
      const month = date.toLocaleDateString("en-US", {
        month: "short",
      });
      return `${day}-${month}`;
    };

    // seal method to handle page information change
    const handleQueryData = async () => {
      data.value = route.query;
      const id = Array.isArray(route.query.id)
        ? route.query.id[0]
        : route.query.id;
      allData.value = await getCityForecastInfoById(Number(id));
      currentDetail.value = allData.value.basic;
      forecastDetail.value = allData.value.forecast;
      isLoaded.value = true;
    };

    // reload page
    onMounted(async () => {
      isLoaded.value = false;
      handleQueryData();
    });

    // listener
    watch(
      () => route.query,
      () => {
        isLoaded.value = false;
        handleQueryData();
      }
    );
    return {
      data,
      currentDetail,
      isLoaded,
      toEnglishDate,
      forecastDetail,
    };
  },
});
</script>

<template>
  <div v-if="isLoaded" class="weather-app">
    <!-- favorite cities -->
    <main class="content">
      <h1>City Information</h1>
      <h2>Today</h2>
      <div class="grid-currentDetail">
        <div class="weather-card detail-cards">
          <div class="city-header">
            <h2>{{ currentDetail.cityname }}</h2>
            <span class="temp">{{ currentDetail.temp }}</span>
          </div>
          <div class="condition">{{ currentDetail.simp_desc }}</div>
          <div class="high-low">
            H:{{ currentDetail.temp_max }} L:{{ currentDetail.temp_min }}
          </div>
        </div>
        <div class="right-block">
          <div>Sun Raise:</div>
          <div>Pressure:</div>
          <div>Feels Like:</div>
        </div>
        <div class="right-block">
          <div>{{ currentDetail.sun_raise }}</div>
          <div>{{ currentDetail.pressure }}</div>
          <div>{{ currentDetail.feels_like }}</div>
        </div>
        <div class="right-block">
          <div>SunSet:</div>
          <div>Humidity:</div>
          <div>Detail</div>
        </div>
        <div class="right-block">
          <div>{{ currentDetail.sun_set }}</div>
          <div>{{ currentDetail.humidy }}</div>
          <div>{{ currentDetail.detail_desc }}</div>
        </div>
      </div>

      <!-- hot cities -->
      <section style="margin-top: 40px">
        <h1>Weather forecast</h1>
        <div class="grid-container">
          <div
            v-for="(forecast, index) in forecastDetail"
            :key="'hot-' + index"
            class="weather-card"
          >
            <div class="city-header">
              <h2>{{ toEnglishDate(forecast.date) }}</h2>
              <span class="temp">{{ forecast.temp }}</span>
            </div>
            <div class="condition">{{ forecast.simp_desc }}</div>
            <div class="high-low">
              H:{{ forecast.temp_max }} L:{{ forecast.temp_min }}
            </div>
          </div>
        </div>
      </section>
    </main>
  </div>
  <div v-else class="loading">
    Loading... <loading-outlined spin style="font-size: 32px; color: #42b983" />
  </div>
</template>

<style scoped>
.grid-container {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-top: 20px;
  padding: 0 20px;
}
.grid-currentDetail {
  gap: 40px;
  margin-top: 20px;
  padding: 0 20px;
  display: flex;
}
.detail-cards {
  width: 24%;
  min-width: 240px;
}
.content h1 {
  text-align: left;
  margin-left: 0;
  margin-top: 30px;
  padding-left: 20px;
  font-size: 1.8rem;
  color: #2c3e50;
  border-bottom: 2px solid #42b983;
  padding-bottom: 0.5rem;
}
.content h2 {
  text-align: left;
  margin-left: 0;
  margin-top: 30px;
  padding-left: 20px;
  font-size: 1.8rem;
  color: #2c3e50;
  padding-bottom: 0.5rem;
}
.weather-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s;
  min-width: 240px;
}
.city-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}
.high-low {
  color: #666;
  margin-top: 8px;
  font-size: 0.9rem;
}
.temp {
  font-size: 1.8rem;
  font-weight: bold;
  color: #42b983;
}
.loading {
  font-size: 1.8rem;
  font-weight: bold;
  margin-top: 50px;
}
.right-block {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  margin-top: 20px;
  margin-left: 50px;
  padding-left: 20px;
  font-size: 1.3rem;
  line-height: 2.2rem;
}
</style>
