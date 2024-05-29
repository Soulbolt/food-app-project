// import { GoSearch } from "react-icons/go";
import { FaHeartCirclePlus } from "react-icons/fa6";
import { FaMapMarkerAlt } from "react-icons/fa";
import React, { useState } from "react";
import SearchBar from "./SearchBar"
import LoginImg from "../assets/breakfast.jpg";
import CardImage from "../assets/kabobs.jpg";

function Dashboard({ restaurants }) {
  const [search, setSearch] = useState("");
  const [filteredRestaurants, setFilteredRestaurants] = useState(restaurants);

/**
 * Handles the search functionality by updating the search state and filtering the restaurants based on the search input.
 *
 * @param {Event} e - The event object triggered by the search input.
 * @return {void} This function does not return anything.
 */
  const handleSearch = (e) => {
    setSearch(e.target.value);
    const filtered = restaurants.filter((restaurant) =>
      restaurant.name.toLowerCase().includes(search.toLowerCase())
    );
    setFilteredRestaurants(filtered);
  };

  /**
   * Handles the submission of the search form by preventing the default form submission behavior.
   *
   * @param {Event} e - The event object representing the form submission event.
   * @return {void} This function does not return anything.
   */
  const handleSearchSubmit = (e) => {
    e.preventDefault();
  };

/**
 * Handles the addition of a restaurant to favorites.
 *
 * @param {number} id - The ID of the restaurant to be added to favorites.
 * @return {void} This function does not return anything.
 */
  const handleAddToFavorites = (id) => {
    const updatedRestaurants = restaurants.map((restaurant) => {
      if (restaurant.id === id) {
        return { ...restaurant, isFavorite: !restaurant.isFavorite };
      }
      return restaurant;
    });
    setFilteredRestaurants(updatedRestaurants);
  };

/**
 * Handles the removal of a restaurant from favorites.
 *
 * @param {number} id - The ID of the restaurant to be removed from favorites.
 * @return {void} This function does not return anything.
 */
  const handleRemoveFromFavorites = (id) => {
    const updatedRestaurants = restaurants.map((restaurant) => {
      if (restaurant.id === id) {
        return { ...restaurant, isFavorite: !restaurant.isFavorite };
      }
      return restaurant;
    });
    setFilteredRestaurants(updatedRestaurants);
  };

/**
 * Handles the click event on a marker and updates the state of the filteredRestaurants array.
 *
 * @param {number} id - The ID of the restaurant associated with the clicked marker.
 * @return {void} This function does not return anything.
 */
  const handleMarkerClick = (id) => {
    const updatedRestaurants = restaurants.map((restaurant) => {
      if (restaurant.id === id) {
        return { ...restaurant, isMarkerClicked: !restaurant.isMarkerClicked };
      }
      return restaurant;
    });
    setFilteredRestaurants(updatedRestaurants);
  };

/**
 * Handles the hover event on a marker and updates the state of the filtered restaurants.
 *
 * @param {number} id - The ID of the restaurant marker being hovered.
 * @return {void} This function does not return anything.
 */
  const handleMarkerHover = (id) => {
    const updatedRestaurants = restaurants.map((restaurant) => {
      if (restaurant.id === id) {
        return { ...restaurant, isMarkerHovered: !restaurant.isMarkerHovered };
      }
      return restaurant;
    });
    setFilteredRestaurants(updatedRestaurants);
  };

  /**
   * Handles the mouse leave event on a marker and updates the state of the filtered restaurants.
   *
   * @param {number} id - The ID of the restaurant marker being hovered.
   * @return {void} This function does not return anything.
   */
  const handleMarkerLeave = (id) => {
    const updatedRestaurants = restaurants.map((restaurant) => {
      if (restaurant.id === id) {
        return { ...restaurant, isMarkerHovered: !restaurant.isMarkerHovered };
      }
      return restaurant;
    });
    setFilteredRestaurants(updatedRestaurants);
  };

  return (
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
      <div className="relative">
        {/* Search Bar Compnent */}
        <SearchBar />

        <div className="flex h-full items-center justify-center">
          <h2 className="mb-8 text-3xl text-indigo-300">
            Recommendations For You!
          </h2>
        </div>

        {/* Recommended - Table Data */}
        <div className="container mx-auto p-4">
          <div className="max-h-[500px] overflow-x-auto">
            <table className="min-w-full bg-white">
              <thead className="bg-gray-800 text-white">
                <tr>
                  <th className="w-1/5 px-4 py-2">Name</th>
                  <th className="w-1/5 px-4 py-2">Address</th>
                  <th className="w-1/5 px-4 py-2">Contact Number</th>
                  <th className="w-1/5 px-4 py-2">Rating</th>
                  <th className="w-1/5 px-4 py-2">Reviews</th>
                </tr>
              </thead>
              <tbody className="text-gray-700">
                {Array.isArray(restaurants) &&
                  restaurants.map((restaurant, index) => (
                    <tr
                      key={index}
                      className={index % 2 === 0 ? "bg-gray-200" : ""}
                    >
                      <td className="border px-4 py-2">{restaurant.name}</td>
                      <td className="border px-4 py-2">{restaurant.address}</td>
                      <td className="border px-4 py-2">
                        {restaurant.contact_number}
                      </td>
                      <td className="border px-4 py-2">{restaurant.rating}</td>
                      <td className="border px-4 py-2">
                        {restaurant.reviews.map((review, index) => (
                          <p key={index}>
                            <strong>{review.username}:</strong> {review.review}
                            (Rating: {review.rating})
                          </p>
                        ))}
                      </td>
                    </tr>
                  ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
      {/*<!-- Glboal Container -->*/}
      {Array.isArray(restaurants) &&
        restaurants.map((restaurant, index) => (
          <div class="mb-3 flex items-center justify-center">
            {/* <!-- Card Container --> */}
            <div class="m-3 flex flex-col space-y-10 rounded-2xl bg-white p-6 shadow-2xl md:m-0 md:flex-row md:space-x-10 md:space-y-0 md:p-16">
              {/*<!-- Image Container -->*/}
              <div>
                <img
                  src={CardImage}
                  alt="kabobs"
                  class="mx-auto w-60 duration-200 hover:scale-105"
                />
              </div>

              {/*<!-- Content -->*/}
              <div class="flex flex-col space-y-6">
                {/*<!-- Label & Title Container-->*/}
                <div class="mb-4 flex flex-col space-y-3 text-center md:text-left">
                  <div class="inline-block rounded-full bg-black px-3 py-1 text-sm text-white">
                    Free Delivery on Orders Above $50
                  </div>
                </div>

                {/*<!-- Title -->*/}
                <div
                  key={index}
                  class="max-w-sm text-center text-4xl font-medium md:text-left"
                >
                  {restaurant.name}
                </div>
                {/*<!-- Price -->*/}
                <div class="mb-4 flex flex-col space-y-3 text-center md:text-left">
                  <p class="text-2xl font-bold">Lunch Special!</p>
                  <p class="line-through">$79</p>
                  <p class="text-4xl font-bold">$49</p>
                  <p class="text-sm-font-light text-gray-400">
                    This offer is valid until the 4th of July!
                  </p>
                </div>

                {/*<!-- Button Group -->*/}
                <div class="group">
                  <button class="w-full rounded-lg border-b-8 border-b-blue-700 bg-blue-700 text-white transition-all duration-150 group-hover:border-b-0 group-hover:border-t-8 group-hover:border-t-blue-700 group-hover:bg-blue-700 group-hover:shadow-lg">
                    <div class="rounded-lg bg-blue-500 px-8 py-4 duration-150 group-hover:bg-blue-700">
                      Check out the reviews!
                    </div>
                  </button>
                </div>

                {/*<!-- Rating Score -->*/}
                <div class="group flex items-center space-x-3">
                  <div class="h-3 w-3 rounded-full bg-green-400 group-hover:animate-ping"></div>
                  <div class="text-sm">
                    <p key={index}>Rating: {restaurant.rating}</p>
                  </div>
                </div>
                {/*<!-- Bottom Buttons Container -->*/}
                <div class="flex flex-col space-y-4 md:flex-row md:space-x-4 md:space-y-0">
                  <button class="flex items-center justify-center space-x-3 rounded-lg border-2 border-gray-300 px-5 py-3 shadow-sm transition-all duration-150 hover:-translate-y-0.5 hover:bg-opacity-30 hover:shadow-lg">
                    <FaMapMarkerAlt class="w-8 text-3xl" />
                    <span>Get Directions</span>
                  </button>

                  <div class="flex flex-col space-y-4 md:flex-row md:space-x-4 md:space-y-0">
                    <button class="flex items-center justify-center space-x-3 rounded-lg border-2 border-gray-300 px-5 py-3 shadow-sm transition-all duration-150 hover:-translate-y-0.5 hover:bg-opacity-30 hover:shadow-lg">
                      <FaHeartCirclePlus class="w-8 text-4xl text-red-600" />
                      <span>Add to Favorites</span>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        ))}
    </div>
  );
}

export default Dashboard;
