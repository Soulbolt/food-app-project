import React from "react";
import kabobs from "../assets/kabobs.jpg";

function Login3() {
  return (
    <div className="flex h-screen w-full">
      <div className="md:grid-cols2 m-auto grid h-[550px] grid-cols-1 shadow-lg shadow-gray-600 sm:max-w-[900px]">
        <div className="hidden h-[550px] w-full md:block">
          <img className="h-full w-full" src={kabobs} alt="kabobs" />
        </div>

        <div>
          <form>
            <h2>My Food</h2>
            <div>
              <input type="text" placeholder="Username" />
              <input type="password" placeholder="Password" />
            </div>
            <button>Sign In</button>
            <p>Forgot Username or Password?</p>
          </form>
          <p>Don't have an account? Sign Up Here!</p>
        </div>
      </div>
    </div>
  );
}

export default Login3;
