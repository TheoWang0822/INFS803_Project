<template>
  <div class="weather-app">
    <main class="content">
      <div v-if="userInfo != null && hotFavCityWeatherList.length">
        <h1>Your favorites</h1>
        <div class="grid-container">
          <div
            v-for="(city, index) in hotFavCityWeatherList"
            :key="index"
            class="weather-card"
            @click="OnHotCityClick(city)"
          >
            <div class="city-header">
              <h2>{{ city.cityname }}</h2>
              <span class="temp">{{ city.temp }}℃</span>
            </div>
            <div class="condition">{{ city.simp_desc }}</div>
            <div class="high-low">
              H:{{ city.temp_max }} L:{{ city.temp_min }}
            </div>
          </div>
        </div>
      </div>

      <section style="margin-top: 40px">
        <h1 style="font-size: 2rem">Hot city</h1>
        <div v-if="hotCityWeatherList.length === 0" class="loading">
          <loading-outlined spin style="font-size: 32px; color: #42b983" />
          Loading...
        </div>
        <div v-else class="grid-container">
          <div
            v-for="(city, index) in hotCityWeatherList"
            :key="'hot-' + index"
            class="weather-card"
            @click="OnHotCityClick(city)"
          >
            <div class="city-header">
              <h2>{{ city.cityname }}</h2>
              <span class="temp">{{ city.temp }}℃</span>
            </div>
            <div class="condition">{{ city.simp_desc }}</div>
            <div class="high-low">
              H:{{ city.temp_max }} L:{{ city.temp_min }}
            </div>
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
import { getAllHotCityInfo, getCityInfoById } from "@/dao/weatherDao";
import { GetUserInfo, GetFavCities } from "@/dao/userDao";
import { LoadingOutlined } from "@ant-design/icons-vue";
import { useRouter } from "vue-router";

/////////////////////////////////////////////////////

interface WeatherData {
  city: string;
  temp: string;
  condition: string;
  high: string;
  low: string;
}

export default defineComponent({
  components: {
    // eslint-disable-next-line vue/no-unused-components
    LoadingOutlined,
  },
  setup() {
    const router = useRouter();
    const favorites = ref<WeatherData[]>([]);
    const hotCities = ref<WeatherData[]>([]);
    const hotCityList = ref<any[]>([]);
    const hotCityWeatherList = ref<any[]>([]);
    const hotFavCityWeatherList = ref<any[]>([]);
    const userInfo = ref<null | { username: string }>(null);
    const OnHotCityClick = (city: any) => {
      //if (userInfo.value != null) {
      router.push({
        name: "details",
        query: { id: city.id },
      });
      return;
      //}
      //router.push("/login");
    };
    onMounted(async () => {
      favorites.value = await weatherDao.getFavorites();
      hotCityList.value = await getAllHotCityInfo();

      const result: any[] = [];
      console.log(hotCityList);
      for (const city of hotCityList.value) {
        try {
          const weather = await getCityInfoById(city.id);
          result.push({ ...weather, cityname: city.cityname });
        } catch (e) {
          console.error(`获取 ${city.cityname} 天气失败`, e);
        }
      }

      hotCityWeatherList.value = result;
      console.log(hotCityWeatherList.value);

      await checkIsLoggedIn();
      window.addEventListener("user-logged-in", checkIsLoggedIn);
      window.addEventListener("user-logged-out", checkIsLoggedIn);

      const weatherArr: any[] = [];

      const raw = await GetFavCities();
      const favCities = Array.isArray(raw) ? raw : [];
      for (const city of favCities) {
        const weather = await getCityInfoById(city.id);
        weather.cityname = city.cityname;
        weather.country = city.country;
        weatherArr.push(weather);
      }
      hotFavCityWeatherList.value = weatherArr;
      console.log("..........", hotFavCityWeatherList.value);
    });
    onBeforeUnmount(() => {
      window.removeEventListener("user-logged-in", checkIsLoggedIn);
      window.removeEventListener("user-logged-out", checkIsLoggedIn);
    });
    async function checkIsLoggedIn() {
      const result: any[] = [];
      try {
        userInfo.value = await GetUserInfo();
        if (userInfo.value != null) {
          console.log("这是测试数据1: ", userInfo.value);
        } else {
          console.log("这是测试数据2: ", userInfo.value);
        }
      } catch {
        userInfo.value = null;
      }
    }
    return {
      favorites,
      hotCities,
      userInfo,
      hotCityWeatherList,
      OnHotCityClick,
      hotFavCityWeatherList,
    };
  },
});
</script>

<style scoped>
/* ============ 根容器 ============ */
.weather-app {
  background: linear-gradient(135deg, #1b2735 0%, #090a0f 100%);
  min-height: 100vh;
  padding-top: 20px;
}

html,
body,
#app {
  background: linear-gradient(135deg, #1b2735 0%, #090a0f 100%);
  height: 100%;
  margin: 0; /* 去掉浏览器默认 8px 外边距，白条就没了 */
}

/* ============ 天气卡片（通用，与详情页统一） ============ */
.weather-card,
.detail-cards {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 16px;
  padding: 16px; /* ⬅ 收窄整体内边距 */
  backdrop-filter: blur(12px);
  box-shadow: 0 4px 16px rgba(0, 255, 255, 0.25);
  color: #00ffe1;
  text-shadow: 0 0 4px #00ffe1;
  transition: transform 0.3s, box-shadow 0.3s;
  min-width: 240px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: flex-start;
  //height: 160px;
}

.weather-card:hover,
.detail-cards:hover {
  transform: scale(1.03);
  box-shadow: 0 8px 28px rgba(0, 255, 255, 0.35);
}

/* ============ 容器布局 ============ */
.grid-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 24px;
  margin-top: 24px;
  padding: 0 20px;
}

.grid-currentDetail {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  gap: 40px;
  margin-top: 20px;
  padding: 0 20px;
}

/* ============ 卡片标题头部（更靠左） ============ */
.city-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  padding: 0;
}

.city-header h2 {
  font-size: 1.5rem;
  margin-left: -10px;
  font-weight: 700;
  color: #00ffe1;
  text-shadow: 0 0 6px #00ffe1;
  flex: 1 1 auto;
  text-align: left;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.temp {
  font-size: 2.2rem;
  font-weight: bold;
  color: #00ffe1;
  text-shadow: 0 0 6px #00ffe1;
  flex-shrink: 0;
  margin-left: 24px;
}

/* ============ 天气内容 ============ */
.condition {
  font-size: 1rem;
  font-weight: 400;
  margin-top: 8px;
  margin-bottom: 4px;
  margin-left: 8px;
  color: #00ffe1;
  text-shadow: 0 0 3px #00ffe1;
  text-align: right;
}

.high-low {
  font-size: 0.95rem;
  font-weight: 300;
  margin-left: 8px;
  display: flex;
  justify-content: flex-start;
  gap: 16px;
  margin-top: 4px;
  color: #00ffe1;
  text-shadow: 0 0 3px #00ffe1;
}

/* ============ 标题样式 ============ */
.content h1,
.content h2 {
  text-align: left;
  margin-top: 30px;
  padding-left: 20px;
  color: #00ffe1;
  padding-bottom: 0.5rem;
  text-shadow: 0 0 6px #00ffe1;
}

/* ============ 右侧信息块（详情页专用） ============ */
.right-blocks-wrapper {
  display: grid;
  grid-template-columns: repeat(2, auto auto);
  grid-template-rows: repeat(2, auto);
  column-gap: 200px;
  row-gap: 50px;
  width: 100%;
  padding: 0 20px;
  margin-top: 30px;
}

.right-block {
  font-size: 1.5rem;
  color: #00ffe1;
  text-shadow: 0 0 3px #00ffe1;
  font-weight: 400;
  line-height: 2rem;
}

/* ============ 加载动画 ============ */
.loading {
  font-size: 1.8rem;
  font-weight: bold;
  margin-top: 50px;
  color: #00ffe1;
  text-align: center;
}
</style>
