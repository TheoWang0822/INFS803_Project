// src/dao/weatherDao.ts

// 1. Define the weather Data
// TODO: modify this after negotiate with James
interface WeatherData {
  city: string;
  temp: string;
  condition: string;
  high: string;
  low: string;
}

// 2. Mocked local data (to replace the real API)
// TODO: modify this after negotiate with James
const mockData = {
  favorites: [
    {
      city: "Auckland",
      temp: "20°",
      condition: "Sunny",
      high: "23°",
      low: "15°",
    },
    {
      city: "Shanghai",
      temp: "16°",
      condition: "Clear",
      high: "28°",
      low: "16°",
    },
    {
      city: "Wellington",
      temp: "21°",
      condition: "Foggy",
      high: "24°",
      low: "18°",
    },
    {
      city: "ChristChurch",
      temp: "18°",
      condition: "Frosty",
      high: "19°",
      low: "16°",
    },
  ],
  hotCities: [
    {
      city: "New York",
      temp: "9°",
      condition: "Cloudy",
      high: "9°",
      low: "1°",
    },
    {
      city: "Paris",
      temp: "9°",
      condition: "Partly Cloudy",
      high: "13°",
      low: "7°",
    },
    // other hot cities etc...
  ],
};

// 3. Achieve Dao method
export default {
  // Get favorite cities' weather
  getFavorites(): Promise<WeatherData[]> {
    return new Promise((resolve) => {
      setTimeout(() => resolve(mockData.favorites), 500); // mock latency
    });
  },

  // Get hot cities' weather
  getHotCities(): Promise<WeatherData[]> {
    return new Promise((resolve) => {
      setTimeout(() => resolve(mockData.hotCities), 500);
    });
  },
};
