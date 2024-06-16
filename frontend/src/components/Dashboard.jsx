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
  const [restaurants, setRestaurants] = useState([]);
  const [recommendedRestaurants, setRecommendedRestaurants] = useState([]);
  const [filteredRestaurant, setFilteredRestaurants] = useState([]);
  const [error, setError] = useState(null);
  const [showRecommended, setShowRecommended] = useState(false);
  const [showAll, setShowAll] = useState(false);
  const [showById, setShowById] = useState(false);
  const [subtitle, setSubtitle] = useState("");
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
        setFilteredRestaurants([]);
        return;
      }

      setIsLoading(true);

      try {
        const filtered = await fetchRestaurantById(search);

        if (!filtered) {
          // Handle not found error
          setError("No restaurant found with the given ID.");
          setFilteredRestaurants([]);
        } else {
          setFilteredRestaurants([filtered]);
          setError(null); // Clear any previous error
        }
      } catch (error) {
        console.error("Error fetching restaurant by ID:", error);
        setError("An error occurred while fetching the restaurant.");
      } finally {
        setIsLoading(false);
        setShowById(true);
        setShowAll(false);
        setShowRecommended(false);
        setSubtitle("Showing Resturant by ID");
      }
    },
    [search],
  );

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
    if (recommendedRestaurants.length === 0) {
      setShowRecommended(true);
      fetchRecommendedRestaurants()
        .then((restaurantList) => {
          setRecommendedRestaurants(restaurantList || []);
          console.log(restaurantList);
          setIsLoading(false);
        })
        .catch((error) => {
          console.error("Error fetching recommended restaurants:", error);
          setError("An error occurred while fetching recommended restaurants.");
          setIsLoading(false);
        });
    }
  }, [recommendedRestaurants]);

  // TODO: (possible refactor)Add array to handle multiple filters aka Show All and Show Recommended
  const handleSelect = useCallback(
    async (value) => {
      console.log("selectedOption in Dashboard:", value);
      if (value === "Show All" && restaurants.length === 0) {
        setIsLoading(true);
        setSubtitle("Showing all restaurants");
        fetchRestaurants()
          .then((restaurantList) => {
            setRestaurants(restaurantList || []);
            setShowRecommended(false); // Hide the recommended restaurants
            setShowById(false);
            setShowAll(true);
            console.log(restaurantList);
            setIsLoading(false);
          })
          .catch((error) => {
            console.error("Error fetching restaurants:", error);
            setError("An error occurred while fetching restaurants.");
            setIsLoading(false);
          });
      } else if (value === "Show All" && restaurants.length > 0) {
        setSubtitle("Showing all restaurants");
        console.log("List of restaurants:", recommendedRestaurants);
        setShowRecommended(false); // Hide the recommended restaurants
        setShowById(false);
        setShowAll(true);
      } else if (value === "Show Recommended") {
        setSubtitle("Your recommended restaurants");
        setRecommendedRestaurants(recommendedRestaurants);
        setShowRecommended(true);
        setShowAll(false);
        setShowById(false);
      } else if (
        value === "Search By ID" &&
        (filteredRestaurant.length === 0 || filteredRestaurant.length === 1)
      ) {
        console.log("search:", search);
        handleSearch();
      } else if (value === "Search By ID" && filteredRestaurant.length > 0) {
        setSubtitle("Showing restaurants by ID");
        setFilteredRestaurants(filteredRestaurant);
        setShowById(true);
        setShowAll(false);
        setShowRecommended(false);
      }
      console.log("subtitle:", subtitle);
    },
    [
      recommendedRestaurants,
      restaurants,
      subtitle,
      filteredRestaurant,
      search,
      handleSearch,
    ],
  );

  if (isLoading) {
    return <Spinner />;
  }

  return (
    <div>
      <div className="h-screen-full w-full bg-slate-900">
        {/* <div
        className="h-screen-full relative w-full bg-zinc-900/90 bg-cover bg-center bg-no-repeat"
        style={{
          backgroundImage: `url(${LoginImg})`,
          backgroundAttachment: "fixed",
        }}
      > */}
        {/* <img
        className="absolute h-full w-full object-cover mix-blend-overlay"
        src={LoginImg}
        alt="breakfast"
      /> */}
        <div className="flex items-center justify-center">
          <h2 className="mb-8 rounded-lg border bg-zinc-900 p-2 text-5xl text-cyan-500">
            Welcome To Your Dashboard
          </h2>
        </div>
        <div className="sticky top-1 z-50">
          {/* Search Bar Compnent */}
          <SearchBar
            search={search}
            setSearch={setSearch}
            handleSearch={handleSearch}
            onSelect={handleSelect}
            error={error}
          />
        </div>
        <div className="relative flex h-full items-center justify-center">
          <h2 className="mb-8 mt-8 rounded-lg border bg-zinc-900 px-2 text-3xl text-cyan-500">
            {subtitle}
          </h2>
        </div>
        {/*<!-- Glboal Container -->*/}
        <div>
          {showRecommended && recommendedRestaurants.length > 0 ? (
            <div>
              <div className="flex flex-wrap justify-center gap-4 p-4">
                {recommendedRestaurants.map((restaurant) => (
                  <RestaurantCard
                    key={restaurant.id}
                    id={restaurant.id}
                    name={restaurant.name}
                    address={restaurant.address}
                    contactNumber={restaurant.contactNumber}
                    rating={restaurant.rating}
                    isFavorite={restaurant.isFavorite}
                    reviews={restaurant.reviews}
                    onAddToFavorites={handleAddToFavorites}
                    onRemoveFromFavorites={handleRemoveFromFavorites}
                  />
                ))}
              </div>
            </div>
          ) : showAll && restaurants.length > 0 ? (
            <div>
              <div className="flex flex-wrap justify-center gap-4 p-4">
                {restaurants.map((restaurant) => (
                  <RestaurantCard
                    key={restaurant.id}
                    id={restaurant.id}
                    name={restaurant.name}
                    address={restaurant.address}
                    contactNumber={restaurant.contactNumber}
                    rating={restaurant.rating}
                    isFavorite={restaurant.isFavorite}
                    reviews={restaurant.reviews}
                    onAddToFavorites={handleAddToFavorites}
                    onRemoveFromFavorites={handleRemoveFromFavorites}
                  />
                ))}
              </div>
            </div>
          ) : showById && filteredRestaurant.length > 0 ? (
            <div>
              <div className="justify-center">
                {filteredRestaurant.map((restaurant) => (
                  <RestaurantCard
                    key={restaurant.id}
                    id={restaurant.id}
                    name={restaurant.name}
                    address={restaurant.address}
                    contactNumber={restaurant.contactNumber}
                    rating={restaurant.rating}
                    isFavorite={restaurant.isFavorite}
                    reviews={restaurant.reviews}
                    onAddToFavorites={handleAddToFavorites}
                    onRemoveFromFavorites={handleRemoveFromFavorites}
                  />
                ))}
              </div>
            </div>
          ) : (
            <div>
              <div className="justify-center">No restaurants found</div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
