import {
  fetchRestaurants,
  fetchRecommendedRestaurants,
  fetchRestaurantById,
  fetchRestaurantsByName,
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
  const [filteredByName, setFilteredRestaurantsByName] = useState([]); // [fetchRestaurantsByName]
  const [error, setError] = useState(null);
  const [showRecommended, setShowRecommended] = useState(false);
  const [showAll, setShowAll] = useState(false);
  const [showById, setShowById] = useState(false);
  const [showByName, setShowByName] = useState(false);
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

      if (search?.trim() === "") {
        setFilteredRestaurants([]);
        setFilteredRestaurantsByName([]);
        return;
      }

      setIsLoading(true);

      try {
        let filtered = [];
        if (Number(search)) {
          console.log("Fetching restaurant by ID:", search);
          filtered = await fetchRestaurantById(search);
          setFilteredRestaurants([filtered]);
          setSubtitle(`Showing results for restaurant with ID ${search}`);
          setIsLoading(false);
          setShowById(true);
          setShowByName(false);
          setShowAll(false);
          setShowRecommended(false);
        } else {
          console.log("Fetching restaurant by name:", search);
          filtered = await fetchRestaurantsByName(search);
          setSubtitle("Showing Resturants by Matching Input:");
          setFilteredRestaurantsByName(filtered);
          setShowByName(true);
          setShowById(false);
          setShowAll(false);
          setShowRecommended(false);
        }

        if (!filtered) {
          // Handle not found error
          setError("No restaurant found with the given input.");
          setFilteredRestaurants([]);
          setFilteredRestaurantsByName([]);
        }
      } catch (error) {
        console.error("Error fetching restaurant by given input:", error);
        setError("An error occurred while fetching the restaurant.");
      } finally {
        setIsLoading(false);
      }
    },
    [
      search,
      setFilteredRestaurants,
      setIsLoading,
      setFilteredRestaurantsByName,
      setError,
    ],
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

  // TODO: (possible refactor)Add array and for loop to handle multiple conditions for filter options.
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
            setShowByName(false);
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
        setShowByName(false);
        setShowAll(true);
      } else if (value === "Show Recommended") {
        setSubtitle("Recommended Restaurants");
        setRecommendedRestaurants(recommendedRestaurants);
        setShowRecommended(true);
        setShowAll(false);
        setShowById(false);
        setShowByName(false);
      } else if (value === "Search By ID") {
        setSearch("");
        setFilteredRestaurantsByName([]);
        // TODO: Figure out a way to reuse state to return/filter by ID
      } else if (value === "Search By Name") {
        setFilteredRestaurants([]);
        setSearch("");
        // TODO: Figure out a way to reuse state to return/filter by Name
      }
    },
    [recommendedRestaurants, restaurants, setSearch],
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
            {subtitle ? subtitle : "Recommended Restaurants"}
          </h2>
        </div>
        {/*<!-- Glboal Container -->*/}
        <div className="flex min-h-screen w-full flex-col">
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
          ) : showByName && filteredByName.length > 0 ? (
            <div>
              <div className="flex flex-wrap justify-center gap-4 p-4">
                {filteredByName.map((restaurant) => (
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
              <div className="justify-center">
                <p>No results found</p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
