import "./App.css";
import axios from "axios";
import { useState, useEffect } from "react";

function App() {
  const [people, setPeople] = useState([]);

  useEffect(() => {
    console.log("insde the useEffect");
    axios.get("/api").then((res) => {
      setPeople(res.data);
      console.log(res.data);
    });
  }, []);

  return people.map((person, index) => {
    return (
      (<h3>People Data Test</h3>),
      (
        <p key={index}>
          {person.id} {person.name} {person.age}
        </p>
      )
    );
  });
}

export default App;
