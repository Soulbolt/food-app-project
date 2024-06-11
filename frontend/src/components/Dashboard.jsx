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
  const [recommendedRestaurants, setRecommendedRestaurants] = useState([]);
  const [filteredRestaurant, setFilteredRestaurants] = useState([]);
  const [error, setError] = useState(null);

  /**
   * Handles the search functionality.
   *
   * @param {Event} e - The event object.
   * @return {Promise<void>} A promise that resolves when the search is complete.
   */
  const handleSearch = useCallback(
    async (e) => {
      e.preventDefault();
      setSearch(e.target.value);

      if (search.trim() === "") {
        setFilteredRestaurants(recommendedRestaurants);
        return;
      }

      setIsLoading(true);

      try {
        const filtered = await fetchRestaurantById(search);

        if (!filtered) {
          // Handle not found error
          setError("No restaurant found with the given ID.");
          setFilteredRestaurants([recommendedRestaurants]);
        } else {
          setError(null); // Clear any previous error
          setFilteredRestaurants([filtered]);
        }
      } catch (error) {
        console.error("Error fetching restaurant by ID:", error);
        setError("An error occurred while fetching the restaurant.");
      } finally {
        setIsLoading(false);
      }
    },
    [search, recommendedRestaurants],
  );

  // May need a single search function.
  // const handleSearchSubmit = useCallback(async () => {
  //   if (!search) {
  //     setFilteredRestaurants(null);
  //     setError(null);
  //     return;
  //   }

  //   const fetchData = async () => {
  //     try {
  //       const response = await fetchRestaurantById(search);
  //       if (response) {
  //         setFilteredRestaurants([response]);
  //         setError(null); // Clear any previous error
  //       } else {
  //         // Handle not found error
  //         setFilteredRestaurants(null);
  //         setError("No restaurant found with the given ID.");
  //       }
  //     } catch (error) {
  //       setFilteredRestaurants(null);
  //       console.error("Error fetching restaurant by ID:", error);
  //       setError("An error occurred while fetching the restaurant.");
  //     }
  //   };

  //   fetchData();
  // }, [search]);
  /**
   * Handles the addition of a restaurant to favorites.
   *
   * @param {number} id - The ID of the restaurant to be added to favorites.
   * @return {void} This function does not return anything.
   */
  const handleAddToFavorites = (id) => {
    setRecommendedRestaurants((prevRestaurants) =>
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
    setRecommendedRestaurants((prevRestaurants) =>
      prevRestaurants.map((restaurant) =>
        restaurant.id === id
          ? { ...restaurant, isFavorite: false }
          : restaurant,
      ),
    );
  };

  useEffect(() => {
    console.log("inside the useEffect");
    fetchRecommendedRestaurants()
      .then((restaurantList) => {
        setRecommendedRestaurants(restaurantList || []);
        setIsLoading(false);
      })
      .catch((error) => {
        console.error("Error fetching recommended restaurants:", error);
        setError("An error occurred while fetching recommended restaurants.");
        setIsLoading(false);
      });
  }, []);

  if (isLoading) {
    return <Spinner />;
  }

  return (
    <div>
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
          <SearchBar
            search={search}
            setSearch={setSearch}
            handleSearch={handleSearch}
          />
        </div>
        <div className="relative flex h-full items-center justify-center">
          <h2 className="mb-8 text-3xl text-indigo-300">
            Recommendations For You!
          </h2>
        </div>
        {/*<!-- Glboal Container -->*/}
        <div>
          {filteredRestaurant ? (
            <RestaurantCard
              key={filteredRestaurant.id}
              {...filteredRestaurant}
              onAddToFavorites={() =>
                handleAddToFavorites(filteredRestaurant.id)
              }
              onRemoveFromFavorites={() =>
                handleRemoveFromFavorites(filteredRestaurant.id)
              }
            />
          ) : (
            Array.isArray(recommendedRestaurants) &&
            recommendedRestaurants.map((restaurant) => (
              <RestaurantCard
                key={restaurant.id}
                {...restaurant}
                onAddToFavorites={() => handleAddToFavorites(restaurant.id)}
                onRemoveFromFavorites={() =>
                  handleRemoveFromFavorites(restaurant.id)
                }
              />
            ))
          )}
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
