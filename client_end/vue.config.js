const { defineConfig } = require("@vue/cli-service");
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    proxy: {
      "/GetStatus": {
        target: "http://localhost:8080",
        changeOrigin: true,
      },
      "/SearchCityByName": {
        target: "http://localhost:8080",
        changeOrigin: true,
      },
      "/GetCurrentWeatherByCity": {
        target: "http://localhost:8080",
        changeOrigin: true,
      },
      "/GetForecastWeatherByCity": {
        target: "http://localhost:8080",
        changeOrigin: true,
      },
      "/Login": {
        target: "http://localhost:8080",
        changeOrigin: true,
      },
      "/Register": {
        target: "http://localhost:8080",
        changeOrigin: true,
      },
      "/GetUserProfile": {
        target: "http://localhost:8080",
        changeOrigin: true,
      },
      "/Logout": {
        target: "http://localhost:8080",
        changeOrigin: true,
      },
      "/AddFavoriteCity": {
        target: "http://localhost:8080",
        changeOrigin: true,
      },
      "/DelFavoriteCity": {
        target: "http://localhost:8080",
        changeOrigin: true,
      },
    },
  },
});
