import "./App.css";
import axios from "axios";
import { useState, useEffect } from "react";

export default function App() {
  const [people, setPeople] = useState([]);

  useEffect(() => {
    console.log("insde the useEffect");
    axios.get("/api").then((res) => {
      setPeople(res.data);
      console.log(res.data);
    });
  }, []);

  return (
    <>
      <h3 className=" text-3xl font-bold text-cyan-500 underline">
        People Data Test
      </h3>

      {people.map((person, index) => (
        <p key={index} className=" text-3xl font-bold text-cyan-500">
          {person.id} {person.name} {person.age}
        </p>
      ))}
    </>
  );
}
