import React, { useState, useRef, useEffect } from 'react'

function SearchBar() {
    const [isSticky, setIsSticky] = useState(false);
    const searchBarRef = useRef(null);

    const handleScroll = () => {
        const scrollTop = window.scrollY;
        const searchBarHeight = searchBarRef.current.offsetHeight || 0;
        setIsSticky(scrollTop > searchBarHeight);
    };

    useEffect(() => {
        window.addEventListener('scroll', handleScroll);
        return () => { window.removeEventListener('scroll', handleScroll); };
    }, []);

    return (
        <div>
            
        </div>
    )
}

export default SearchBar
