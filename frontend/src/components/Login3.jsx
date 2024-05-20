import React from "react";
import kabobs from "../assets/kabobs.jpg";
function Login3() {
  return (
    <div>
      <div>
        <img src={kabobs} alt="kabobs" />
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
  );
}

export default Login3;
