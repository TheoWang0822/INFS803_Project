<template>
  <div class="weather-app">
    <!-- 显示返回按钮 -->
    <!-- 收藏城市 -->
    <!-- 网格布局容器 -->
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

      <!-- 热门城市 -->
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

    <!--    &lt;!&ndash; 热门城市 &ndash;&gt;
    <section>
      <h2>Hot cities</h2>
      <div v-for="city in hotCities" :key="city.city" class="city-card">
        <h3>{{ city.city }}</h3>
        <p>{{ city.temp }} {{ city.condition }}</p>
        <small>H:{{ city.high }} L:{{ city.low }}</small>
      </div>
    </section>-->
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
/* 新增网格布局样式 */
.grid-container {
  display: grid;
  grid-template-columns: repeat(3, 1fr); /* 每行3列 */
  gap: 20px; /* 卡片间距 */
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
  transform: translateY(-3px); /* 悬停效果 */
}

/* 调整文字样式 */
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

/* 保持原有导航栏样式不变 */
.nav-bar {
  /* ... */
}

/* 新增标题左对齐样式 */
.content h1 {
  text-align: left;
  margin-left: 0;
  padding-left: 0;
  font-size: 1.8rem;
  color: #2c3e50;
  border-bottom: 2px solid #42b983; /* 可选：添加下划线装饰 */
  padding-bottom: 0.5rem;
}
</style>
