<!-- src/components/NavBar.vue -->
<template>
  <nav class="nav-bar">
    <img
      v-if="showBackButton"
      src="/images/logo2.png"
      alt=""
      class="back-button"
      @click="goToHome"
    />
    <div class="nav-links">
      <router-link to="/">Home</router-link> |
      <router-link to="/about">About</router-link>
    </div>

    <div class="input-pos">
      <a-select
        show-search
        v-model:value="selectedCity"
        placeholder="Search city"
        :options="cityOptions"
        :filter-option="false"
        :not-found-content="fetching ? 'Loading...' : null"
        @search="handleSearch"
        @change="handleSelect"
      />
    </div>
    <div class="login">
      <template v-if="!userInfo">
        <UserOutlined @click="onRightClicked" />
        Login
      </template>
      <template v-else><UserOutlined @click="logout" /> Logout </template>
    </div>
  </nav>
</template>

<script lang="ts">
import { defineComponent, onMounted, onBeforeUnmount } from "vue";
import { useRouter } from "vue-router";
import { getCityInfo } from "@/dao/weatherDao";
import { GetUserInfo, Logout } from "@/dao/userDao";
import { ref } from "vue";
//////////////////////////////

import { debounce } from "lodash-es";
import { UserOutlined } from "@ant-design/icons-vue";

////////////////////////////

export default defineComponent({
  components: {
    UserOutlined,
  },
  name: "NavBar",
  props: {
    showBackButton: {
      type: Boolean,
      default: false, // Default not display
    },
  },
  setup() {
    const router = useRouter();
    const searchValue = ref<string>("");
    ////////////////////////////////////////////////////////////////////////////
    const selectedCity = ref<string>("");
    const cityOptions = ref<{ label: string; value: string }[]>([]);
    const fetching = ref(false);
    const isLoggedIn = ref(false);
    const userInfo = ref<null | { username: string }>(null);
    async function checkIsLoggedIn() {
      try {
        userInfo.value = await GetUserInfo();
      } catch {
        userInfo.value = null;
      }
    }
    async function logout() {
      const logoutCB = () => {
        userInfo.value = null;
      };
      Logout(logoutCB);
      router.push("/");
    }
    onMounted(() => {
      checkIsLoggedIn();
      window.addEventListener("user-logged-in", checkIsLoggedIn);
    });
    onBeforeUnmount(() => {
      window.removeEventListener("user-logged-in", checkIsLoggedIn);
    });
    //async function logout(){}
    const handleSearch = debounce(async (input: string) => {
      if (input.length < 3) {
        cityOptions.value = [];
        return;
      }
      fetching.value = true;
      try {
        const response = await getCityInfo(input); // 假设是数组
        cityOptions.value = response.slice(0, 10).map((city: any) => ({
          label: `${city.cityname}, ${city.country}`,
          value: String(city.id),
        }));
      } catch (e) {
        console.error("City search failed", e);
      } finally {
        fetching.value = false;
      }
    }, 300); //300ms

    const onRightClicked = () => {
      if (isLoggedIn.value) {
        return;
      }
      router.push("/login");
    };

    const handleSelect = (value: string) => {
      router.push({
        name: "details",
        query: {
          id: value,
        },
      });
    };
    ////////////////////////////////////////////////////////////////////////////////
    const onSearch = async (value: string) => {
      const response = await getCityInfo(value);
      if (Object.keys(response).length !== 0) {
        router.push({
          name: "details",
          query: {
            id: response[0].id,
            cityname: response[0].cityname,
            country: response[0].country,
          },
        });
      } else {
        alert("No city found!");
      }
    };

    const goToHome = () => {
      searchValue.value = "";
      selectedCity.value = "";
      router.push("/");
    };

    return {
      goToHome,
      searchValue,
      onSearch,
      selectedCity,
      cityOptions,
      fetching,
      handleSearch,
      handleSelect,
      UserOutlined,
      onRightClicked,
      isLoggedIn,
      userInfo,
      logout,
    };
  },
});
</script>

<style scoped>
.nav-bar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 100px;
  z-index: 1000;
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 15px 30px;
  background: rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  width: 100vw;
  box-sizing: border-box;
  color: #ffffff;
  box-shadow: 0 4px 12px rgba(0, 255, 255, 0.1);
}

.back-button {
  cursor: pointer;
  transition: transform 0.2s ease;
  height: 100%;
  aspect-ratio: 1;
}

.back-button:hover {
  transform: scale(1.1);
}

.nav-links {
  font-size: 1.2rem;
  color: #ffffff;
}

.nav-links a {
  color: #00ffe1;
  font-size: 22px;
  font-weight: 600;
  text-decoration: none;
  margin: 0 10px;
  transition: color 0.2s;
}

.nav-links a:hover {
  color: #00bfa6;
}

.nav-links a.router-link-exact-active {
  color: #ffffff;
}

.input-pos {
  flex: 1;
  display: flex;
  justify-content: center;
}

.input-pos .ant-select {
  flex: 1 1 400px;
  min-width: 50px;
  max-width: 500px;
  margin-right: 200px;
}

.login {
  display: flex;
  cursor: pointer;
  gap: 8px;
  font-size: 22px;
  color: #00ffe1;
  position: absolute;
  right: 40px;
  transition: color 0.2s ease;
  margin-right: 20px;
}

.login:hover {
  color: #00bfa6;
}
</style>
