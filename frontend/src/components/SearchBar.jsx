import React, { useState } from "react";

function SearchBar({ search, setSearch, optionSelected, handleSearch, error }) {
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const [selectedOption, setSelectedOption] = useState("");

  const toggleDropdown = () => {
    setDropdownOpen((dropdownOpen) => !dropdownOpen);
  };

  const handleOptionSelect = (event) => {
    console.log("Option selected:", event);
    setSelectedOption(event);
    toggleDropdown();
  };

  return (
    <div className="relative">
      <form onSubmit={handleSearch} className="mx-auto max-w-lg">
        <div className="flex">
          <label className="sr-only mb-2 text-sm font-medium text-gray-900 dark:text-white">
            Your Email
          </label>
          <button
            id="dropdown-button"
            onClick={toggleDropdown}
            onChange={(e) => optionSelected(e.target.value)}
            className="inline-flex flex-shrink-0 items-center rounded-s-lg border border-gray-300 bg-gray-100 px-4 py-2.5 text-center text-sm font-medium text-gray-900 hover:bg-gray-200 focus:outline-none focus:ring-1 focus:ring-gray-100 dark:border-gray-600 dark:bg-gray-700 dark:text-white dark:hover:bg-gray-600 dark:focus:ring-gray-700"
            type="button"
          >
            {selectedOption || "Options"}
            <svg
              className="ms-2.5 h-2.5 w-2.5"
              aria-hidden="true"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 10 6"
            >
              <path
                stroke="currentColor"
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="m1 1 4 4 4-4"
              />
            </svg>
          </button>
          <div
            id="dropdown"
            className="display-none absolute top-11 rounded-lg bg-white shadow dark:bg-gray-700"
          >
            {dropdownOpen && (
              <ul
                className="left-0 p-2 text-sm text-gray-700 dark:text-gray-200 "
                aria-labelledby="dropdown-button"
              >
                <li
                  className="px-4 py-1 hover:bg-gray-200 focus:outline-none focus:ring-4 focus:ring-gray-100 dark:border-gray-600 dark:bg-gray-700 dark:text-white dark:hover:bg-gray-600 dark:focus:ring-gray-700"
                  onClick={() => handleOptionSelect("Show All")}
                >
                  Show All
                </li>
                <li
                  className="px-4 py-1 hover:bg-gray-200 focus:outline-none focus:ring-4 focus:ring-gray-100 dark:border-gray-600 dark:bg-gray-700 dark:text-white dark:hover:bg-gray-600 dark:focus:ring-gray-700"
                  onClick={() => handleOptionSelect("Search By Name")}
                >
                  Search By Name
                </li>
                <li
                  className="px-4 py-1 hover:bg-gray-200 focus:outline-none focus:ring-4 focus:ring-gray-100 dark:border-gray-600 dark:bg-gray-700 dark:text-white dark:hover:bg-gray-600 dark:focus:ring-gray-700"
                  onClick={() => handleOptionSelect("Search Category")}
                >
                  Search Category
                </li>
                <li
                  className="px-4 py-1 hover:bg-gray-200 focus:outline-none focus:ring-4 focus:ring-gray-100 dark:border-gray-600 dark:bg-gray-700 dark:text-white dark:hover:bg-gray-600 dark:focus:ring-gray-700"
                  onClick={() => handleOptionSelect("Search By Id")}
                >
                  Search By Id
                </li>
              </ul>
            )}
          </div>
          <div className="relative w-full">
            <input
              type="search"
              id="search-dropdown"
              value={search || ""}
              onChange={(e) => setSearch(e.target.value)}
              className="z-20 block w-full rounded-e-lg border border-s-2 border-gray-300 border-s-gray-50 bg-gray-50 p-2.5 text-sm text-gray-900 focus:border-blue-500 focus:ring-blue-500 dark:border-gray-600 dark:border-s-gray-700  dark:bg-gray-700 dark:text-white dark:placeholder-gray-400 dark:focus:border-blue-500"
              placeholder={!error ? "Click options to search" : "Whoops..."}
              required
            />
            <button
              type="submit"
              className="absolute end-0 top-0 h-full rounded-e-lg border border-blue-700 bg-blue-700 p-2.5 text-sm font-medium text-white hover:bg-blue-800 focus:outline-none focus:ring-4 focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
            >
              <svg
                className="h-4 w-4"
                aria-hidden="true"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 20 20"
              >
                <path
                  stroke="currentColor"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  d="m19 19-4-4m0-7A7 7 0 1 1 1 8a7 7 0 0 1 14 0Z"
                />
              </svg>
              <span className="sr-only">Search</span>
            </button>
          </div>
        </div>

        {error && (
          <div className="bg-gray-50 text-red-500 dark:bg-red-200">{error}</div>
        )}
      </form>
    </div>
  );
}

export default SearchBar;
