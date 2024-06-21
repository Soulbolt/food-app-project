import React from "react";
import { FaHeartCirclePlus, FaHeartCrack, FaPhone } from "react-icons/fa6";
import { FaMapMarkerAlt } from "react-icons/fa";
import { MdLocationCity } from "react-icons/md";
import CardImage from "../assets/kabobs.jpg";

function RestaurantCard({
  id,
  name,
  address,
  contact_number,
  rating,
  isFavorite,
  reviews,
  onAddToFavorites,
  onRemoveFromFavorites,
}) {
  const [showModal, setShowModal] = React.useState(false);

  return (
    <div className="mb-3 flex items-center justify-center">
      {/* <!-- Card Container --> */}
      <div className="m-3 flex flex-col space-y-10 rounded-2xl bg-white p-6 shadow-2xl md:m-0 md:flex-row md:space-x-10 md:space-y-0 md:p-16">
        {/*<!-- Image Container -->*/}
        <div>
          <img
            src={CardImage}
            alt="kabobs"
            className="mx-auto w-60 duration-200 hover:scale-105"
          />
        </div>

        {/*<!-- Content -->*/}
        <div className="flex flex-col space-y-6">
          {/*<!-- Label & Title Container-->*/}
          <div className="mb-4 flex flex-col space-y-3 text-center md:text-left">
            <div className="inline-block rounded-full bg-black px-3 py-1 text-sm text-white">
              Free Delivery on Orders Above $50
            </div>
          </div>

          {/*<!-- Title -->*/}
          <div className="max-w-sm text-center text-4xl font-medium md:text-left">
            {name}
            <p className="mb-2 mt-2 flex flex-auto text-2xl text-gray-400">
              <MdLocationCity className="mr-2 text-5xl text-zinc-600" />
              {address}
            </p>
            <p className="flex flex-auto text-2xl text-gray-400">
              <FaPhone className="mr-2 mt-2 text-lime-500" />
              {contact_number}
            </p>
          </div>
          {/*<!-- Price -->*/}
          <div className="mb-4 flex flex-col space-y-3 text-center md:text-left">
            <p className="text-2xl font-bold">Lunch Special!</p>
            <p className="line-through">$79</p>
            <p className="text-4xl font-bold">$49</p>
            <p className="text-sm-font-light text-gray-400">
              This offer is valid until the 4th of July!
            </p>
          </div>

          {/*<!-- Button Group -->*/}
          <div className="group">
            <button
              className="w-full rounded-lg border-b-8 border-b-blue-700 bg-blue-700 text-white transition-all duration-150 group-hover:border-b-0 group-hover:border-t-8 group-hover:border-t-blue-700 group-hover:bg-blue-700 group-hover:shadow-lg"
              onClick={() => setShowModal(true)}
            >
              <div className="rounded-lg bg-blue-500 px-8 py-4 duration-150 group-hover:bg-blue-700">
                Check out the reviews!
              </div>
            </button>
          </div>

          {/*<!-- Modal -->*/}
          {showModal && (
            <div className="fixed left-0 top-0 flex h-full w-full items-center justify-center bg-black bg-opacity-50">
              <div className="rounded-lg bg-white p-8">
                <h2 className="text-3xl font-bold">Reviews</h2>
                <ul>
                  {reviews.map((review) => (
                    <li
                      key={review.id}
                      className="my-2 border-4 border-slate-300 p-2"
                    >
                      <div className="flex flex-col items-start">
                        <label className="text-l font-bold">User:</label>
                        <p>{review.username}</p>
                        <label className="text-l font-bold">Review:</label>
                        <p>{review.review}</p>
                        <label className="text-l font-bold">Rating:</label>
                        <p>{review.rating}</p>
                      </div>
                    </li>
                  ))}
                </ul>
                <button
                  className="mt-4 rounded-lg bg-blue-500 px-4 py-2 text-white"
                  onClick={() => setShowModal(false)}
                >
                  Close
                </button>
              </div>
            </div>
          )}

          {/*<!-- Rating Score -->*/}
          <div className="group flex items-center space-x-3">
            <div className="h-3 w-3 rounded-full bg-green-400 group-hover:animate-ping"></div>
            <div className="text-sm">
              <p>Rating: {rating}</p>
            </div>
          </div>
          {/*<!-- Bottom Buttons Container -->*/}
          <div className="flex flex-col space-y-4 md:flex-row md:space-x-4 md:space-y-0">
            <button className="flex items-center justify-center space-x-3 rounded-lg border-2 border-gray-300 px-5 py-3 shadow-sm transition-all duration-150 hover:-translate-y-0.5 hover:bg-opacity-30 hover:shadow-lg">
              <FaMapMarkerAlt className="w-8 text-3xl" />
              <span>Get Directions</span>
            </button>

            <div className="flex flex-col space-y-4 md:flex-row md:space-x-4 md:space-y-0">
              {isFavorite ? (
                <button
                  onClick={onRemoveFromFavorites}
                  className="flex items-center justify-center space-x-3 rounded-lg border-2 border-gray-300 px-5 py-3 shadow-sm transition-all duration-150 hover:-translate-y-0.5 hover:bg-opacity-30 hover:shadow-lg"
                >
                  <FaHeartCrack className="w-8 text-4xl text-red-600" />
                  <span>Remove from Favorites</span>
                </button>
              ) : (
                <button
                  onClick={onAddToFavorites}
                  className="flex items-center justify-center space-x-3 rounded-lg border-2 border-gray-300 px-5 py-3 shadow-sm transition-all duration-150 hover:-translate-y-0.5 hover:bg-opacity-30 hover:shadow-lg"
                >
                  <FaHeartCirclePlus className="w-8 text-4xl text-red-600" />
                  <span>Add to Favorites</span>
                </button>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default RestaurantCard;
