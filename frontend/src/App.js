import { BrowserRouter, Routes, Route } from "react-router-dom";
import React, { useState, useEffect } from "react";
import axios from "axios";
import Dashboard from "./components/Dashboard";
import Login from "./components/Login";

function App() {
  const [restaurants, setRestaurants] = useState([]);

  useEffect(() => {
    console.log("insde the useEffect");
    fetchRestaurants();
  }, []);

  const fetchRestaurants = async () => {
    try {
      const response = await axios.get("/api/restaurants");
      const restaurantList = response.data.map((restaurant) => {
        return {
          ...restaurant,
          isFavorite: false,
          id: restaurant.id,
        };
      });
      setRestaurants(restaurantList);
      console.log(restaurantList);
    } catch (error) {
      console.log("Error fetching data", error);
    }
  };

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route
          path="/dashboard"
          element={<Dashboard restaurants={restaurants} />}
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
