import axios from "axios";

export async function fetchRestaurants() {
  try {
    const response = await axios.get("/api/restaurants");
    const restaurantList = response.data.map((restaurant) => {
      return {
        ...restaurant,
        isFavorite: false,
        id: restaurant.id,
      };
    });
    console.log("The list:", restaurantList);
    return restaurantList;
  } catch (error) {
    console.log("Error fetching data", error);
  }
}

export async function fetchRecommendedRestaurants() {
  try {
    const response = await axios.get("/api/restaurants/recommended");
    const restaurantList = response.data.map((restaurant) => {
      return {
        ...restaurant,
        isFavorite: false,
        id: restaurant.id,
      };
    });
    return restaurantList;
  } catch (error) {
    console.log("Error fetching data", error);
  }
}

export async function fetchRestaurantById(id) {
  try {
    const response = await axios.get(`/api/restaurant/${id}`);
    const restaurant = response.data;
    console.log(restaurant);
    return restaurant;
  } catch (error) {
    console.log("Error fetching data", error);
  }
}

export async function fetchRecommendedRestaurantById(id) {
  try {
    const response = await axios.get(`/api/recommended_restaurant/${id}`);
    const restaurant = response.data;
    return restaurant;
  } catch (error) {
    console.log("Error fetching data", error);
  }
}

export async function fetchRestaurantsByName(name) {
  try {
    const response = await axios.get(`/api/restaurants_by_name/${name}`);
    const restaurantList = response.data.map((restaurant) => {
      return {
        ...restaurant,
        isFavorite: false,
        id: restaurant.id,
      };
    });
    return restaurantList;
  } catch (error) {
    console.log("Error fetching data", error);
  }
}
