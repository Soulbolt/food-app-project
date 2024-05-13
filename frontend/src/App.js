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
      <h1 className="mx-auto mb-10 text-5xl text-cyan-600 lg:text-6xl">
        Welcome to Food App
      </h1>
      <h3 className="mx-auto flex items-center justify-center text-3xl text-cyan-500 underline lg:text-6xl">
        People Data Test
      </h3>

      {people.map((person, index) => (
        <p key={index} className=" text-3xl text-cyan-500 lg:text-6xl">
          {person.id} {person.name} {person.age}
        </p>
      ))}
    </>
  );
}
