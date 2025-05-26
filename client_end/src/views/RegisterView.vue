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
const cb = () => {
  router.push("/login");
};
// submit function
const OnSubmitClicked = async () => {
  await Register(username.value, password.value, 1, email.value, cb);
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
</style>
