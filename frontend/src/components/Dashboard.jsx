import React from "react";
import LoginImg from "../assets/breakfast.jpg";

function Dashboard() {
  return (
    <div className="relative h-screen w-full bg-zinc-900/90">
      <img
        className="absolute h-full w-full object-cover"
        src={LoginImg}
        alt="breakfast"
      />
    </div>
  );
}

export default Dashboard;
