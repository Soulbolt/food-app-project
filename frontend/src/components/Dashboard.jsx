import {
  fetchRestaurants,
  fetchRecommendedRestaurants,
  fetchRestaurantById,
} from "../services/apiRestaurants";
import Spinner from "./Spinner";
import React, { useState, useEffect, useCallback } from "react";
import SearchBar from "./SearchBar";
import LoginImg from "../assets/breakfast.jpg";
import RestaurantCard from "./RestaurantCard";

function Dashboard() {
  const [isLoading, setIsLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [restaurant, setRestaurant] = useState([]);
  const [recommendedRestaurants, setRecommendedRestaurants] = useState([]);
  const [filteredRestaurants, setFilteredRestaurants] = useState([]);

  /**
   * Handles the search functionality by updating the search state and filtering the restaurants based on the search input.
   *
   * @param {Event} e - The event object triggered by the search input.
   * @return {void} This function does not return anything.
   */
  const handleSearch = async (e) => {
    e.preventDefault();
    const searchTerm = e.target.value;
    setSearch(searchTerm);

    if (searchTerm.trim() === "") {
      setFilteredRestaurants(recommendedRestaurants);
      return;
    }

    try {
      const filtered = await fetchRestaurantById(searchTerm);
      setFilteredRestaurants([filtered]);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  /**
   * Handles the addition of a restaurant to favorites.
   *
   * @param {number} id - The ID of the restaurant to be added to favorites.
   * @return {void} This function does not return anything.
   */
  const handleAddToFavorites = (id) => {
    setRestaurant((prevRestaurants) =>
      prevRestaurants.map((restaurant) =>
        restaurant.id === id ? { ...restaurant, isFavorite: true } : restaurant,
      ),
    );
  };

  /**
   * Handles the removal of a restaurant from favorites.
   *
   * @param {number} id - The ID of the restaurant to be removed from favorites.
   * @return {void} This function does not return anything.
   */
  const handleRemoveFromFavorites = (id) => {
    setRestaurant((prevRestaurants) =>
      prevRestaurants.map((restaurant) =>
        restaurant.id === id
          ? { ...restaurant, isFavorite: false }
          : restaurant,
      ),
    );
  };

  useEffect(() => {
    console.log("inside the useEffect");
    fetchRecommendedRestaurants().then((restaurantList) => {
      setRecommendedRestaurants(restaurantList);
      // setFilteredRestaurants(restaurantList);
      setIsLoading(false);
    });
  }, []);

  useEffect(() => {
    console.log("inside the useEffect for fetchById with id", id);
    if (id === 0) {
      return;
    }
    const fetchData = async () => {
      console.log("inside the useEffect for fetchById");
      try {
        const response = await fetchRestaurantById(id);
        setRestaurant(response);
      } catch (error) {
        console.log("Error fetching data", error);
      }
    };
    fetchData();
  }, [id]);

  if (!restaurant) {
    return (
      <div>
        <Spinner />
      </div>
    );
  }

  return (
    <div>
      {isLoading ? (
        <Spinner />
      ) : (
        <div
          className="h-screen-full relative w-full bg-zinc-900/90 bg-cover bg-center bg-no-repeat"
          style={{
            backgroundImage: `url(${LoginImg})`,
            backgroundAttachment: "fixed",
          }}
        >
          {/* <img
        className="absolute h-full w-full object-cover mix-blend-overlay"
        src={LoginImg}
        alt="breakfast"
      /> */}

          <div>
            <h2 className="mb-8 py-8 text-5xl text-indigo-300">
              Welcome To Your Dashboard
            </h2>
          </div>
          <div className="sticky top-0 z-50">
            {/* Search Bar Compnent */}
            <SearchBar search={search} handleSearch={handleSearch} />
          </div>
          <div className="relative flex h-full items-center justify-center">
            <h2 className="mb-8 text-3xl text-indigo-300">
              Recommendations For You!
            </h2>
          </div>
          {/*<!-- Glboal Container -->*/}
          {Array.isArray(recommendedRestaurants) &&
            recommendedRestaurants.map((restaurant) => (
              <RestaurantCard
                key={restaurant.id}
                {...restaurant}
                onAddToFavorites={handleAddToFavorites}
                onRemoveFromFavorites={handleRemoveFromFavorites}
              />
            ))}
        </div>
      )}
    </div>
  );
}

export default Dashboard;
