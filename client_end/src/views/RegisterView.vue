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
body {
  background: linear-gradient(to bottom right, #f5f7fa, #e6ecf3);
}
</style>

<style scoped>
.input-bars {
  width: 320px;
  margin: 100px auto;
}
.input-row {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 6px;
  width: 100%;
  margin-bottom: 20px;
}
.fonts {
  font-weight: 600;
  font-size: 16px;
  margin-left: 4px;
  color: #333;
}
</style>
