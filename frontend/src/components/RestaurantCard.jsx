import React from "react";
import {
  FaHeart,
  FHeartBroken,
  FaMapMarkerAlt,
  FaPhoneAlt,
} from "react-icons/fa";

function RestaurantCard({
  name,
  address,
  contactNumber,
  rating,
  isFvorite,
  onAddToFavorites,
  onRemoveFromFavorites,
}) {
  return (
    <div className="m-4 max-w-sm overflow-hidden rounded bg-white p-4 shadow-lg">
      <div className="px-6 py-4">
        <div className="mb-2 text-xl font-bold">{name}</div>
        <p className="text-base text-gray-700">
          <FaMapMarkerAlt className="mr-2 inline-block" />
          {address}
        </p>
        <p className="text-base text-gray-700">
          <FaPhoneAlt className="mr-2 inline-block" />
          {contactNumber}
        </p>
        <p className="text-base text-gray-700">Rating: {rating}</p>
      </div>
      <div className="px-6 pb-2 pt-4">
        {isFvorite ? (
          <button
            className="mb-2 rounded bg-red-500 px-4 py-2 font-bold text-white hover:bg-red-700"
            onClick={onRemoveFromFavorites}
          >
            Remove from Favorites
          </button>
        ) : (
          <button
            className="mb-2 rounded bg-blue-500 px-4 py-2 font-bold text-white hover:bg-blue-700"
            onClick={onAddToFavorites}
          >
            Add to Favorites
          </button>
        )}
      </div>
    </div>
  );
}

export default RestaurantCard;
