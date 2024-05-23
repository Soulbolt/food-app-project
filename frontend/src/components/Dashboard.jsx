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

        {/* Previous Seaches - Table Data */}
        <div className="container mx-auto p-4">
          <div className="overflow-x-auto">
            <table className="min-w-full bg-white">
              <thead className="bg-gray-800 text-white">
                <tr>
                  <th className="w-1/5 px-4 py-2">Name</th>
                  <th className="w-1/5 px-4 py-2">Address</th>
                  <th className="w-1/5 px-4 py-2">Contact Number</th>
                  <th className="w-1/5 px-4 py-2">Rating</th>
                  <th className="w-1/5 px-4 py-2">Reviews</th>
                </tr>
              </thead>
              <tbody className="text-gray-700">
                <tr>
                  <td className="border px-4 py-2">The Gourmet Kitchen</td>
                  <td className="border px-4 py-2">
                    123 Maple Street, Springfiel, IL 62705
                  </td>
                  <td className="border px-4 py-2">(215) 555-0198</td>
                  <td className="border px-4 py-2">4.5</td>
                  <td className="border px-4 py-2">
                    Amazing food and great ambiance!
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        {/* <table className="table-auto">
          <thead>
            <tr className="flex-cols-2 sm:flex-cols-5 overflow-x-hidden">
              <th className="border p-8 text-indigo-300">Restaurant</th>
              <th className="border p-8 text-indigo-300">Address</th>
              <th className="border p-8 text-indigo-300">City</th>
              <th className="border p-8 text-indigo-300">Zip Code</th>
              <th className="border p-8 text-indigo-300">Phone</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td className="border p-8 text-indigo-300">PlaceHolder</td>
              <td className="border p-8 text-indigo-300">PlaceHolder</td>
              <td className="border p-8 text-indigo-300">PlaceHolder</td>
              <td className="border p-8 text-indigo-300">PlaceHolder</td>
              <td className="border p-8 text-indigo-300">PlaceHolder</td>
            </tr>
          </tbody>
        </table> */}
      </div>
    </div>
  );
}

export default Dashboard;
