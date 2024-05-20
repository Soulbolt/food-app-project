import React from "react";
import kabobs from "../assets/kabobs.jpg";

function Login3() {
  return (
    <div className="flex h-screen w-full">
      <div className="m-auto grid h-[550px] grid-cols-1 shadow-lg shadow-gray-600 sm:max-w-[900px] md:grid-cols-2">
        <div className="hidden h-[550px] w-full md:block">
          <img className="h-full w-full" src={kabobs} alt="kabobs" />
        </div>

        <div className="flex flex-col justify-around p-4">
          <form>
            <h2 className="mb-8 text-center text-4xl font-bold">My Food</h2>
            <div>
              <input
                className="mr-2 border p-2"
                type="text"
                placeholder="Username"
              />
              <input
                className="border p-2"
                type="password"
                placeholder="Password"
              />
            </div>
            <button className="my-4 w-full bg-green-600 py-2 hover:bg-green-500">
              Sign In
            </button>
            <p>Forgot Username or Password?</p>
          </form>
          <p>Don't have an account? Sign Up Here!</p>
        </div>
      </div>
    </div>
  );
}

export default Login3;
