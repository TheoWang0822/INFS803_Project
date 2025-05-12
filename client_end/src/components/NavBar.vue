<!-- src/components/NavBar.vue -->
<template>
  <nav class="nav-bar">
    <img
      v-if="showBackButton"
      src="/images/weather-app.png"
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
        style="width: 400px"
      />
    </div>
    <div class="login">
      <template v-if="userInfo">
        <UserOutlined @click="onRightClicked" />
        Login
      </template>
      <template v-else><UserOutlined @click="logout" /> Logout </template>
    </div>
  </nav>
</template>

<script lang="ts">
import { defineComponent, onMounted } from "vue";
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
    }
    onMounted(() => {
      checkIsLoggedIn();
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
  z-index: 1000;
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 15px 20px;
  background: #f8f9fa;
  border-bottom: 1px solid #ddd;
  margin: 0;
  width: 100vw;
  box-sizing: border-box;
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

.input-pos {
  flex: 10;
  display: flex;
  justify-content: center;
  padding-right: 150px;
}

.login {
  display: flex;
  align-items: center;
  cursor: pointer;
  gap: 6px;
  font-size: 20px;
  color: #333;
  position: absolute;
  right: 60px;
}
</style>
