import React from "react";
import { FcGoogle } from "react-icons/fc";
import { AiFillFacebook } from "react-icons/ai";
import LoginImg from "../assets/login-healthy-options.jpg";

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
          <div className="flex justify-between py-8">
            <p className="relative flex items-center border px-6 py-2 shadow-lg hover:shadow-xl">
              <AiFillFacebook className="mr-2" /> Facebook
            </p>
            <p className="relative flex items-center border px-6 py-2 shadow-lg hover:shadow-xl">
              <FcGoogle className="mr-2" /> Google
            </p>
          </div>
          <div className="mb-4 flex flex-col">
            <label className="flex justify-start">Username</label>
            <input type="text" className="relative border bg-gray-100 p-2" />
          </div>
          <div className="flex flex-col">
            <label className="flex justify-start">Password</label>
            <input
              type="password"
              className="relative border bg-gray-100 p-2"
            />
          </div>
          <button className="relative mt-8 w-full bg-indigo-600 py-3 text-white hover:bg-indigo-500">
            Sign In
          </button>
          <p className="relative mt-2 flex items-center">
            <input type="checkbox" className="mr-2" />
            Remember Me
          </p>
          <p className="relative mt-8 text-center">Not a member? Sign up now</p>
        </form>
      </div>
    </div>
  );
}

export default Login2;
