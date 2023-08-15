// import { useForm } from "react-hook-form";
import axios from "axios";
import { useState } from "react";
import { useNavigate } from "react-router-dom";

import useAuth from "../hooks/useAuth";

const Login = () => {
  const [apiError, setApiError] = useState();
  const [data, setData] = useState({
    email: "",
    password: "",
  });

  const { setAuth } = useAuth();

  let navigate = useNavigate();

  const handleChange = (e) => {
    setData({ ...data, [e.target.name]: e.target.value });
  };

  const getUserData = async (token) => {
    const customConfig = {
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    };
    const response = await axios.post(
      "http://127.0.0.1:8010/users/me",
      {},
      customConfig
    );
    if (response.statusText === "OK") {
      let userData = await response.data;
      console.log(userData);
      userData["token"] = token;
      setAuth(userData);
      setApiError(null);
      navigate("/", { replace: true });
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const response = await axios.post(
      "http://127.0.0.1:8010/users/login",
      data
    );

    console.log(response.statusText);
    // if the login is successful - get the token and then get the remaining data from the /me route
    if (response.statusText === "OK") {
      const token = await response.data;
      localStorage.setItem(JSON.stringify(token));
      await getUserData(token["token"]);
    } else {
      let errorResponse = response;
      setApiError(errorResponse["detail"]);
      setAuth(null);
    }
  };

  return (
    <div className="mx-auto p-10 rounded-lg shadow-2xl">
      <h2 className="text-xl text-primary text-center font-bold my-2">
        Login page
      </h2>

      <form onSubmit={handleSubmit}>
        <div className="flex flex-col justify-center items-center">
          <input
            type="text"
            placeholder="email@email.com"
            className="input input-bordered input-accent w-full max-w-xs m-3"
            name="email"
            onChange={handleChange}
            autoComplete="off"
            required
          />

          <input
            type="password"
            placeholder="your password"
            className="input input-bordered input-accent w-full max-w-xs m-3"
            name="password"
            onChange={handleChange}
            required
          />

          <button
            type="submit"
            className="btn btn-outline btn-accent m-3 btn-block"
          >
            Login
          </button>
        </div>
      </form>

      {apiError && (
        <div className="alert alert-error shadow-lg">
          <div>
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="stroke-current flex-shrink-0 h-6 w-6"
              fill="none"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"
              />
            </svg>
            <span>{apiError}</span>
          </div>
        </div>
      )}
    </div>
  );
};

export default Login;
