<template>
  <a-space direction="vertical" class="input-bars">
    <div class="input-row">
      <span class="fonts">Username:</span>
      <a-input v-model:value="username" placeholder="Enter your username" />
    </div>
    <div class="input-row">
      <span class="fonts">Password: </span>
      <a-input
        type="password"
        v-model:value.lazy="password"
        autofocus
        placeholder="Enter your password"
      />
    </div>
    <a-button type="primary" @click="OnLoginClicked">Login</a-button>
    <a-button type="link" @click="OnRegisterClicked"
      >Don't have an account?</a-button
    >
  </a-space>
</template>

<script setup lang="ts">
import { watch, ref } from "vue";
import { useRouter } from "vue-router";
const router = useRouter();
const username = ref<string>("");
const password = ref<string>("");
const OnLoginClicked = () => {
  console.log("clicked");
};
const OnRegisterClicked = () => {
  router.push("/register");
};
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
