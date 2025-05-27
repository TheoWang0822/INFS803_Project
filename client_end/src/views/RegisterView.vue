<template>
  <a-space direction="vertical" class="input-bars">
    <div class="input-row">
      <span class="fonts">Username:</span>
      <a-input v-model:value="username" placeholder="Enter your username" />
    </div>
    <div class="input-row">
      <span class="fonts">Enter your Password: </span>
      <a-input
        type="password"
        v-model:value.lazy="password"
        autofocus
        placeholder="Enter your password"
      />
    </div>
    <div class="input-row">
      <span class="fonts">Confirm your Password: </span>
      <a-input
        type="password"
        v-model:value.lazy="rePassword"
        placeholder="Confirm your password"
      />
    </div>
    <div class="input-row">
      <span class="fonts">Email:</span>
      <a-input v-model:value="email" placeholder="Enter your email" />
    </div>
    <span class="fonts">Choose your character:</span>
    <div class="avatar-container">
      <div class="avatar-slider">
        <div
          v-for="n in 9"
          :key="n"
          @click="avatarId = n"
          :class="['avatar-item', { selected: avatarId === n }]"
        >
          <img :src="`/Avatar/p${n}.png`" :alt="`avatar ${n}`" />
        </div>
      </div>
    </div>

    <a-button type="primary" :disabled="!canSubmit" @click="OnSubmitClicked"
      >Register</a-button
    >
  </a-space>
</template>

<script setup lang="ts">
import { watch, ref, computed } from "vue";
import { Register } from "@/dao/userDao";
import router from "@/router";
const username = ref<string>("");
const password = ref<string>("");
const rePassword = ref<string>("");
const email = ref<string>("");
// 默认选中第 1 个头像
const avatarId = ref(1);
const cb = () => {
  router.push("/login");
};
// submit function
const OnSubmitClicked = async () => {
  await Register(
    username.value,
    password.value,
    avatarId.value,
    email.value,
    cb
  );
};
const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
const canSubmit = computed(() => {
  return (
    pattern.test(email.value.trim()) &&
    email.value.trim() &&
    username.value.trim() &&
    password.value.trim() &&
    rePassword.value.trim() &&
    password.value === rePassword.value
  );
});
</script>

<style>
.input-bars {
  width: 360px;
  margin: 140px auto; /* 垂直下移并水平居中 */
  display: flex;
  flex-direction: column;
  gap: 28px;
}

.input-row {
  display: flex;
  flex-direction: column;
  gap: 8px;
  width: 100%;
}

.fonts {
  font-size: 18px;
  font-weight: 600;
  color: #00ffe1;
  text-shadow: 0 0 4px #00ffe1;
}

/* --- Ant Design 输入框 ---- */
:deep(.ant-input) {
  background: rgba(255, 255, 255, 0.08) !important;
  border: 1px solid rgba(255, 255, 255, 0.18) !important;
  color: #00ffe1 !important;
  box-shadow: 0 2px 6px rgba(0, 255, 255, 0.15) inset;
}

/* --- 主按钮 ---- */
:deep(.ant-btn-primary) {
  width: 100%;
  background: #00ffe1;
  border: none;
  color: #0c111b;
  font-weight: 600;
}

:deep(.ant-btn-primary:hover) {
  background: #00bfa6;
}

.avatar-container {
  border: 2px solid #00ffe1; /* 外框霓虹青蓝 */
  border-radius: 0.5rem;
  padding: 4px;
  overflow: hidden; /* 隐藏滚动条以外部分 */
  max-width: 360px;
  margin: 0 auto; /* 居中 */
}

.avatar-slider {
  display: flex;
  gap: 12px;
  overflow-x: auto; /* 横向滚动 */
  padding-bottom: 4px; /* 留出滚动条空间 */
}

/* 自定义滚动条样式（WebKit 浏览器） */
.avatar-slider::-webkit-scrollbar {
  height: 8px;
}
.avatar-slider::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
}
.avatar-slider::-webkit-scrollbar-thumb {
  background: rgba(0, 255, 225, 0.7);
  border-radius: 4px;
}

.avatar-item img {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  border: 2px solid transparent;
  cursor: pointer;
}
.avatar-item.selected img {
  border-color: #00ffe1; /* 高亮选中 */
}
</style>
