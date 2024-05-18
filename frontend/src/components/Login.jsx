import React, { useState } from "react";
import LoginImg from "../assets/login-healthy-options.jpg";
import { useNavigate } from "react-router-dom";

function Login() {
  
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  function handleSubmit(e) {
    e.preventDefault();
    if (username === "user" && password === "admin") {
      navigate("/dashboard");
    } else {
      alert("Wrong username or password");
    }
  }

  return (
    <div className="grid h-screen w-full grid-cols-1 sm:grid-cols-2">
      <div className="hidden sm:block">
        <img
          src={LoginImg}
          alt="login"
          className="h-full w-full object-cover"
        />
      </div>

      <div className="flex flex-col justify-center bg-gray-100">
        <form
          action="submit"
          className="mx-auto w-full max-w-[400px] bg-white p-4"
          onSubmit={handleSubmit}
        >
          <h2 className="py-6 text-center text-4xl font-bold">My Food</h2>
          <div className="flex flex-col py-2">
            <label>Username</label>
            <input type="text" value={username} 
            onChange={(e) => setUsername(e.target.value)}
            className="border border-slate-300 p-2" />
          </div>
          <div className="flex flex-col py-2">
            <label>Password</label>
            <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} className="border border-slate-300 p-2" />
          </div>
          <button className="my-5 w-full border bg-indigo-600 py-2 text-white hover:bg-indigo-500">
            Login
          </button>
          <div className="flex justify-between">
            <p className="flex items-center">
              <input type="checkbox" className="mr-2" />
              Remember Me
            </p>
            <button>Create an account</button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default Login;
