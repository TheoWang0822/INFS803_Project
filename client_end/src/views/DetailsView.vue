<script lang="ts">
import { useRoute } from "vue-router";
import { defineComponent, onMounted, ref, watch } from "vue";
import weatherDao, { getCityInfoById } from "@/dao/weatherDao";
import { LoadingOutlined } from "@ant-design/icons-vue";

export default defineComponent({
  components: {
    LoadingOutlined,
  },
  setup() {
    const route = useRoute();
    const data = ref({});
    const tempDetail = ref<any>(null);
    const isLoaded = ref(false);

    // seal method to handle page information change
    const handleQueryData = async () => {
      data.value = route.query;
      const id = Array.isArray(route.query.id)
        ? route.query.id[0]
        : route.query.id;
      tempDetail.value = await getCityInfoById(Number(id));
      isLoaded.value = true;
      console.log("handling new query", tempDetail.value);
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
      tempDetail,
      isLoaded,
    };
  },
});
</script>

<template>
  <div v-if="isLoaded" class="weather-app">
    <!-- favorite cities -->
    <main class="content">
      <h1>City Information</h1>
      <div class="grid-container">
        <div class="weather-card">
          <div class="city-header">
            <h2>{{ data.cityname }}</h2>
            <span class="temp">{{ tempDetail.temp }}</span>
          </div>
          <div class="condition">{{ tempDetail.simp_desc }}</div>
          <div class="high-low">
            H:{{ tempDetail.temp_max }} L:{{ tempDetail.temp_min }}
          </div>
        </div>
      </div>

      <!--      &lt;!&ndash; hot cities &ndash;&gt;
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
      </section>-->
    </main>
  </div>
  <div v-else class="loading">
    Loading... <loading-outlined spin style="font-size: 32px; color: #42b983" />
  </div>
</template>

<style scoped>
.grid-container {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin-top: 20px;
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
.weather-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s;
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
</style>
