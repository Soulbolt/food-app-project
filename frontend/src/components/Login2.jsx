import React from "react";
import LoginImg from "../assets/breakfast.jpg";

function Login2() {
  return (
    <div className="relative h-screen w-full bg-zinc-900/90">
      <img
        className="absolute h-full w-full object-cover mix-blend-overlay"
        src={LoginImg}
        alt=""
      />

      <div>
        <form>
          <h2>My Food</h2>
          <div>
            <p>ICON. Facebook</p>
            <p>ICON. Google</p>
          </div>
          <div>
            <label>Username</label>
            <input type="text" />
          </div>
          <div>
            <label>Password</label>
            <input type="password" />
          </div>
        </form>
      </div>
    </div>
  );
}

export default Login2;
