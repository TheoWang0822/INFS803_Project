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
    <div ref="recaptchaRef"></div>
    <a-button type="primary" @click="OnLoginClicked">Login</a-button>
    <a-button type="link" @click="OnRegisterClicked"
      >Don't have an account?</a-button
    >
  </a-space>
</template>

<script setup lang="ts">
import { watch, ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { Login } from "@/dao/userDao";

const router = useRouter();
const username = ref<string>("");
const password = ref<string>("");
const recaptchaRef = ref<HTMLElement | null>(null);
const recaptchaWidgetId = ref<number | null>(null);
const siteKey = "6LcYLEwrAAAAAIJLwBN28hVFAyMI6KQO1_azxMnK";
const cb = () => {
  router.push("/");
};

onMounted(() => {
  if (typeof grecaptcha !== "undefined" && recaptchaRef.value) {
    // eslint-disable-next-line no-undef
    recaptchaWidgetId.value = grecaptcha.render(recaptchaRef.value, {
      sitekey: siteKey,
    });
  }
});

const OnLoginClicked = () => {
  if (recaptchaWidgetId.value !== null) {
    // eslint-disable-next-line no-undef
    const captchaResponse = grecaptcha.getResponse(recaptchaWidgetId.value);

    if (!captchaResponse) {
      alert("failed to authenticate!");
      return;
    }
    Login(username.value, password.value, cb);
  } else {
    alert("authentication is loading, try later");
  }
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
/* ------ 登录页整体容器 ------ */
.input-bars {
  width: 360px;
  margin: 140px auto; /* 垂直下移一些，水平居中 */
  display: flex;
  flex-direction: column;
  gap: 28px;
}

.input-row {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 8px;
  width: 100%;
}

.fonts {
  font-weight: 600;
  font-size: 18px;
  color: #00ffe1;
  text-shadow: 0 0 4px #00ffe1;
}

:deep(.ant-input) {
  background: rgba(255, 255, 255, 0.08) !important;
  border: 1px solid rgba(255, 255, 255, 0.18) !important;
  color: #00ffe1 !important;
  box-shadow: 0 2px 6px rgba(0, 255, 255, 0.15) inset;
}

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

:deep(.ant-btn-link) {
  color: #00ffe1;
  padding-left: 0;
}

:deep(.ant-btn-link:hover) {
  color: #00bfa6;
}
</style>
