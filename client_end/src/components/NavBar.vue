<!-- src/components/NavBar.vue -->
<template>
  <nav class="nav-bar">
    <!-- 返回按钮 -->
    <img
      v-if="showBackButton"
      src="/images/weather-app.png"
      alt=""
      class="back-button"
      @click="goToHome"
    />

    <!-- 导航链接 -->
    <div class="nav-links">
      <router-link to="/">Home</router-link> |
      <router-link to="/about">About</router-link>
    </div>
  </nav>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { useRouter } from "vue-router";

export default defineComponent({
  name: "NavBar",
  props: {
    showBackButton: {
      type: Boolean,
      default: false, // 默认不显示返回按钮
    },
  },
  setup() {
    const router = useRouter();

    // 返回首页的方法
    const goToHome = () => {
      router.push("/");
    };

    return {
      goToHome,
    };
  },
});
</script>

<style scoped>
/* 复用原有导航栏样式 */
.nav-bar {
  position: fixed; /* 固定定位 */
  top: 0;
  left: 0;
  right: 0; /* 横向撑满 */
  z-index: 1000; /* 确保导航栏在最顶层 */
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 15px 20px;
  background: #f8f9fa;
  border-bottom: 1px solid #ddd;
  margin: 0; /* 消除默认外边距 */
  width: 100vw; /* 强制覆盖父容器限制 */
  box-sizing: border-box; /* 防止padding影响宽度 */
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
</style>
