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
      const response = await axios.get("/api");
      setRestaurants(response.data);
      console.log(response.data);
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

/* <h1 className="mx-auto mb-10 text-5xl text-cyan-600 lg:text-6xl">
        Welcome to Food App
      </h1>
      <h3 className="mx-auto mb-5 items-center justify-center text-3xl text-cyan-500 underline lg:text-5xl">
        Data Test
      </h3>

      <tabe className="mx-auto border-separate border-spacing-2 border border-slate-500 text-2xl text-cyan-500 lg:text-4xl">
        <thead>
          <tr>
            <th className="pr-5">ID</th>
            <th className="pr-5">Name</th>
            <th className="pr-5">Last Name</th>
            <th className="pr-5">Age</th>
          </tr>
        </thead>
        {people.map((person, index) => (
          <tbody key={index}>
            <td>{person.id}</td>
            <td>{person.first_name}</td>
            <td>{person.last_name}</td>
            <td>{person.age}</td>
          </tbody>
        ))}
      </tabe> */
