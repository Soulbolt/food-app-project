import React from "react";
import LoginImg from "../assets/breakfast.jpg";

function Dashboard() {
  return (
    <div className="relative h-screen w-full bg-zinc-900/90">
      <img
        className="absolute h-full w-full object-cover mix-blend-overlay"
        src={LoginImg}
        alt="breakfast"
      />

      <div>
        <h2 className="text-5xl text-indigo-300">Welcome To Your Dashboard</h2>
      </div>
    </div>
  );
}

export default Dashboard;
