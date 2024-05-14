import LoginImg from "../assets/login-healthy-options.jpg";

export default function login() {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2">
      <div>
        <img src={LoginImg} alt="login" />
      </div>

      <div>
        <form action="">
          <h2>BRAND</h2>
          <div>
            <label htmlFor="">Username</label>
            <input type="text" className="border border-slate-300" />
          </div>
        </form>
      </div>
    </div>
  );
}
