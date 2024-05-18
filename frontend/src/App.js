// import axios from "axios";
import Login from "./components/Login";
import Dashboard from "./components/Dashboard";
import { BrowserRouter, Routes, Route } from "react-router-dom";
// import { useState, useEffect } from "react";

function App() {
  // const [people, setPeople] = useState([]);

  // useEffect(() => {
  //   console.log("insde the useEffect");
  //   axios.get("/api").then((res) => {
  //     setPeople(res.data);
  //     console.log(res.data);
  //   });
  // }, []);

  return (<BrowserRouter>
  <Routes>
    <Route path="/" element={<Login />} />
    <Route path="/dashboard" element={<Dashboard />} />
  </Routes>
  </BrowserRouter>);
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
