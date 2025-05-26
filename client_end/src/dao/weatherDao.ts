interface WeatherData {
  city: string;
  temp: string;
  condition: string;
  high: string;
  low: string;
}

const mockData = {
  favorites: [
    {
      city: "Auckland",
      temp: "20",
      condition: "Sunny",
      high: "23°",
      low: "15°",
    },
    {
      city: "Shanghai",
      temp: "16",
      condition: "Clear",
      high: "28°",
      low: "16°",
    },
    {
      city: "Wellington",
      temp: "21",
      condition: "Foggy",
      high: "24°",
      low: "18°",
    },
    {
      city: "ChristChurch",
      temp: "18",
      condition: "Frosty",
      high: "19°",
      low: "16°",
    },
  ],
  hotCities: [
    {
      city: "New York",
      temp: "9",
      condition: "Cloudy",
      high: "9°",
      low: "1°",
    },
    {
      city: "Paris",
      temp: "9",
      condition: "Partly Cloudy",
      high: "13°",
      low: "7°",
    },
    // other hot cities etc...
  ],
};

import axios from "axios";
export async function getCurrentTime() {
  const response = await axios.get("/api/getStatus/");
  return response.data;
}

export async function getCityInfo(str: string) {
  const response = await axios.get("/api/SearchCityByName/", {
    params: {
      cityname: str,
    },
  });
  return response.data.cities;
}

export async function getAllHotCityInfo() {
  const response = await axios.get("/api/SearchCityByName/", {
    params: {
      is_default: 1,
    },
  });
  return response.data.cities;
}

export async function getCityInfoById(id: number) {
  const response = await axios.get("/api/GetCurrentWeatherByCity/", {
    params: {
      id: id,
    },
  });
  return response.data;
}

export async function getCityForecastInfoById(id: number) {
  const response = await axios.get("/api/GetForecastWeatherByCity/", {
    params: {
      id: id,
    },
  });
  return response.data;
}

export default {
  getFavorites(): Promise<WeatherData[]> {
    return new Promise((resolve) => {
      setTimeout(() => resolve(mockData.favorites), 500); // mock latency
    });
  },

  getHotCities(): Promise<WeatherData[]> {
    return new Promise((resolve) => {
      setTimeout(() => resolve(mockData.hotCities), 500);
    });
  },
};
