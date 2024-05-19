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

      <div className="flex h-full items-center justify-center">
        <form className="mx-auto w-full max-w-[400px] bg-white p-8">
          <h2 className="py-8 text-center text-4xl font-bold">My Food</h2>
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
          <button>Sign In</button>
          <p>
            <input type="checkbox" />
            Remember Me
          </p>
          <p>Not a member? Sign up now</p>
        </form>
      </div>
    </div>
  );
}

export default Login2;
