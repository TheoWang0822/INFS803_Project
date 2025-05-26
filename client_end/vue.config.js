const { defineConfig } = require("@vue/cli-service");
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    proxy: {
      "/GetStatus": {
        target: "http://3.104.76.167:8080",
        changeOrigin: true,
      },
      "/SearchCityByName": {
        target: "http://3.104.76.167:8080",
        changeOrigin: true,
      },
      "/GetCurrentWeatherByCity": {
        target: "http://3.104.76.167:8080",
        changeOrigin: true,
      },
      "/GetForecastWeatherByCity": {
        target: "http://3.104.76.167:8080",
        changeOrigin: true,
      },
      "/Login": {
        target: "http://3.104.76.167:8080",
        changeOrigin: true,
      },
      "/Register": {
        target: "http://3.104.76.167:8080",
        changeOrigin: true,
      },
      "/GetUserProfile": {
        target: "http://3.104.76.167:8080",
        changeOrigin: true,
      },
      "/Logout": {
        target: "http://3.104.76.167:8080",
        changeOrigin: true,
      },
      "/AddFavoriteCity": {
        target: "http://3.104.76.167:8080",
        changeOrigin: true,
      },
      "/DelFavoriteCity": {
        target: "http://3.104.76.167:8080",
        changeOrigin: true,
      },
    },
  },
});
