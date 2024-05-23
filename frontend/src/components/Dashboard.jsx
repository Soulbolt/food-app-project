import React from "react";
import LoginImg from "../assets/breakfast.jpg";
import { GoSearch } from "react-icons/go";

function Dashboard() {
  return (
    <div className="relative h-screen w-full bg-zinc-900/90">
      <img
        className="absolute h-full w-full object-cover mix-blend-overlay"
        src={LoginImg}
        alt="breakfast"
      />

      <div>
        <h2 className="mb-8 py-8 text-5xl text-indigo-300">
          Welcome To Your Dashboard
        </h2>
      </div>
      <div className="relative">
        <form class="mx-auto max-w-md">
          <label
            for="default-search"
            class="sr-only mb-2 text-sm font-medium text-gray-900 dark:text-white"
          >
            Search
          </label>
          <div class="relative">
            <div class="pointer-events-none absolute inset-y-0 start-0 flex items-center ps-3">
              <GoSearch className="dark:placeholder-text-gray-400 h-4 w-4 text-gray-500" />
              {/* <svg
                class="h-4 w-4 text-gray-500 dark:text-gray-400"
                aria-hidden="true"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 20 20"
              >
                <path
                  stroke="currentColor"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="m19 19-4-4m0-7A7 7 0 1 1 1 8a7 7 0 0 1 14 0Z"
                />
              </svg> */}
            </div>
            <input
              type="search"
              id="default-search"
              class="mb-8 block w-full rounded-lg border border-gray-300 bg-gray-50 p-4 ps-10 text-sm text-gray-900 focus:border-blue-500 focus:ring-blue-500 dark:border-gray-600 dark:bg-gray-700 dark:text-white dark:placeholder-gray-400 dark:focus:border-blue-500 dark:focus:ring-blue-500"
              placeholder="Search Breakfast, Lunch or Dinner..."
              required
            />
            <button
              type="submit"
              class="absolute bottom-2.5 end-2.5 rounded-lg bg-blue-700 px-4 py-2 text-sm font-medium text-white hover:bg-blue-800 focus:outline-none focus:ring-4 focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
            >
              Search
            </button>
          </div>
        </form>

        <div className="flex h-full items-center justify-center">
          <h2 className="mb-8 text-4xl text-indigo-400">
            Previous searches...
          </h2>
        </div>
        <table className="mx-auto justify-center border-collapse">
          <thead>
          <tr>
          <th className="text-indigo-300 p-8 border">Restaurant</th>
          <th className="text-indigo-300 p-8 border">Address</th>
          <th className="text-indigo-300 p-8 border">City</th>
          <th className="text-indigo-300 p-8 border">Zip Code</th>
          <th className="text-indigo-300 p-8 border">Phone</th>
          </tr>
          </thead>
          <tbody>
          <tr>
            <td className="text-indigo-300 p-8 border">PlaceHolder</td>
            <td className="text-indigo-300 p-8 border">PlaceHolder</td>
            <td className="text-indigo-300 p-8 border">PlaceHolder</td>
            <td className="text-indigo-300 p-8 border">PlaceHolder</td>
            <td className="text-indigo-300 p-8 border">PlaceHolder</td>
          </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default Dashboard;
