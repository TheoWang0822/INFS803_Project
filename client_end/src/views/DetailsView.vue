<script lang="ts">
import { useRoute } from "vue-router";
import { defineComponent, onMounted, ref, watch } from "vue";
import weatherDao, { getCityForecastInfoById } from "@/dao/weatherDao";
import { LoadingOutlined } from "@ant-design/icons-vue";
import { GetUserInfoFav, addFav, delFav } from "@/dao/userDao";

export default defineComponent({
  components: {
    LoadingOutlined,
  },
  setup() {
    const route = useRoute();
    const q = route.query.id;
    const cityId = Number(Array.isArray(q) ? q[0] : q);
    const data = ref({});
    const allData = ref<any>(null);
    const currentDetail = ref<any>(null);
    const forecastDetail = ref<any>(null);
    const isLoaded = ref(false);
    const subscribed = ref(false);
    const userInfo = ref<null | { username: string }>(null);
    const toEnglishDate = (dateString: string) => {
      const date = new Date(dateString);
      const day = date.getDate().toString().padStart(2, "0");
      const month = date.toLocaleDateString("en-US", {
        month: "short",
      });
      return `${day}-${month}`;
    };
    async function checkSubscribed() {
      try {
        userInfo.value = await GetUserInfoFav(cityId);
        if (userInfo.value != null) {
          //TODO: 不为空代表关注了
          subscribed.value = true;
        } else {
          // TODO: 代表没关注
          subscribed.value = false;
        }
      } catch {
        userInfo.value = null;
      }
    }
    const onBtnClick = async () => {
      if (subscribed.value) {
        //TODO: 已订阅
        await delFav(cityId, cbDel);
        return;
      }
      //TODO: 未订阅
      await addFav(cityId, cbAdd);
    };

    const cbAdd = () => {
      subscribed.value = true;
    };
    const cbDel = () => {
      subscribed.value = false;
    };

    // seal method to handle page information change
    const handleQueryData = async () => {
      data.value = route.query;
      allData.value = await getCityForecastInfoById(Number(cityId));
      currentDetail.value = allData.value.basic;
      forecastDetail.value = allData.value.forecast;
      isLoaded.value = true;
    };

    // reload page
    onMounted(async () => {
      isLoaded.value = false;
      handleQueryData();
      checkSubscribed();
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
      onBtnClick,
      subscribed,
    };
  },
});
</script>

<template>
  <div v-if="isLoaded" class="weather-app">
    <main class="content">
      <h1>City Information</h1>
      <div class="today-bar">
        <h2>Today</h2>
      </div>
      <div class="grid-currentDetail">
        <div class="weather-card detail-cards">
          <div class="city-header">
            <h2>{{ currentDetail.cityname }}</h2>
            <span class="temp">{{ currentDetail.temp }}℃</span>
          </div>
          <div class="condition">
            {{ currentDetail.simp_desc }}
          </div>
          <div class="high-low today-bar">
            H:{{ currentDetail.temp_max }} L:{{ currentDetail.temp_min }}
            <a-button type="primary" class="fav-btn" @click="onBtnClick">
              {{ subscribed ? "unFav&nbsp;" : "Save&nbsp;to&nbsp;Fav" }}
            </a-button>
          </div>
        </div>
        <div class="right-blocks-wrapper">
          <div class="right-block">
            <div>Sun Raise:</div>
            <div>Pressure:</div>
            <div>Feels Like:</div>
          </div>
          <div class="right-block">
            <div>{{ currentDetail.sun_raise }}</div>
            <div>{{ currentDetail.pressure }}hPa</div>
            <div>{{ currentDetail.feels_like }}℃</div>
          </div>
          <div class="right-block">
            <div>SunSet:</div>
            <div>Humidity:</div>
            <div>Detail</div>
          </div>
          <div class="right-block">
            <div>{{ currentDetail.sun_set }}</div>
            <div>{{ currentDetail.humidy }}%</div>
            <div>{{ currentDetail.detail_desc }}</div>
          </div>
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
              <span class="temp">{{ forecast.temp }}℃</span>
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
.weather-app {
  background: linear-gradient(135deg, #1b2735 0%, #090a0f 100%);
  min-height: 100vh;
  padding-top: 20px;
  color: white;
}

.grid-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 24px;
  margin-top: 24px;
  padding: 0 20px;
}

.grid-currentDetail {
  flex-direction: row;
  gap: 40px;
  margin-top: 20px;
  padding: 0 20px;
  display: flex;
  flex-wrap: wrap;
}

.weather-card,
.detail-cards {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  padding: 20px;
  backdrop-filter: blur(10px);
  box-shadow: 0 4px 12px rgba(0, 255, 255, 0.15);
  color: #ffffff;
  transition: transform 0.3s, box-shadow 0.3s;
  min-width: 240px;
  max-width: 360px;

  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-between;
}

.weather-card:hover,
.detail-cards:hover {
  transform: scale(1.03);
  box-shadow: 0 8px 28px rgba(0, 255, 255, 0.25);
}

.content h1,
.content h2 {
  text-align: left;
  margin-top: 30px;
  padding-left: 20px;
  font-size: 2rem;
  color: #00ffe1;
  /*border-bottom: 2px solid #00ffe1;*/
  padding-bottom: 0.5rem;
  text-shadow: 0 0 4px #00ffe1;
}

.city-header {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  padding: 0 8px;
  margin-bottom: 8px;
}

.city-header h2 {
  font-size: 1.6rem;
  font-weight: 700;
  margin: 0;
  padding: 0;
  color: #00ffe1;
  text-shadow: 0 0 6px #00ffe1;
  border: none;
  flex: 1;
  text-align: left;
}

.temp {
  font-size: 2.2rem;
  font-weight: bold;
  color: #00ffe1;
  text-shadow: 0 0 6px #00ffe1;
  flex-shrink: 0;
  margin-left: 24px;
}

.condition,
.high-low {
  width: 100%;
  padding: 0 8px;
  color: #00ffe1;
  text-shadow: 0 0 3px #00ffe1;
}

.condition {
  font-weight: 500;
  font-size: 1rem;
  text-align: right;
  margin-bottom: 4px;
}

.high-low {
  font-size: 0.95rem;
  font-weight: 300;
  display: flex;
  justify-content: flex-start;
  gap: 16px;
  margin-top: 4px;
  color: #00ffe1;
  text-shadow: 0 0 3px #00ffe1;
}

/* 核心更新：右侧信息网格 */
.right-blocks-wrapper {
  display: grid;
  grid-template-columns: repeat(2, auto auto);
  grid-template-rows: repeat(2, auto);
  column-gap: 150px;
  row-gap: 20px;
  width: 100%;
  padding: 0 20px;
  margin-top: 50px;
  width: auto;
}

.right-block {
  font-size: 1.5rem;
  color: #00ffe1;
  text-shadow: 0 0 3px #00ffe1;
  font-weight: 400;
  line-height: 2rem;
}

.loading {
  font-size: 1.8rem;
  font-weight: bold;
  margin-top: 50px;
  color: #00ffe1;
  text-align: center;
}

.today-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  margin-top: 30px;
}

.today-bar h2 {
  margin: 0;
  font-size: 2rem;
  color: #00ffe1;
  text-shadow: 0 0 6px #00ffe1;
}

/* ------- 按钮本身 ------- */
:deep(.fav-btn) {
  background: #00ffe1;
  border: none;
  color: #0c111b;
  font-weight: 600;
}

:deep(.fav-btn:hover) {
  background: #00bfa6;
}
</style>
