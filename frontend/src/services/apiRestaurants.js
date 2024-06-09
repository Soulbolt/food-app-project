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
    console.log("The list:", restaurantList);
    return restaurantList;
  } catch (error) {
    console.log("Error fetching data", error);
  }
}
