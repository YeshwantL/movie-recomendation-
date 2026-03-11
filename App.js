const { useState, useEffect } = React;

const apiBase = 'http://localhost:5000'; // Flask backend URL

function Carousel({ title, movies }) {
  return (
    <div className="carousel">
      <h2>{title}</h2>
      <div className="carousel-container">
        {movies.map(movie => (
          <div key={movie.id} className="movie-card">
            <img
              src={movie.poster_path || 'https://via.placeholder.com/200x300?text=No+Image'}
              alt={movie.title}
              className="poster"
            />
            <p>{movie.title}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

function App() {
  const [popularMovies, setPopularMovies] = useState([]);
  const [genreMovies, setGenreMovies] = useState({});
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const genres = ["Action", "Comedy", "Drama", "Horror", "Romance", "Sci-Fi"];

  useEffect(() => {
    fetch(`${apiBase}/movies/popular`)
      .then(res => res.json())
      .then(setPopularMovies)
      .catch(console.error);

    genres.forEach(genre => {
      fetch(`${apiBase}/recommend?genre=${encodeURIComponent(genre)}`)
        .then(res => res.json())
        .then(data => {
          setGenreMovies(prev => ({ ...prev, [genre]: data }));
        })
        .catch(console.error);
    });
  }, []);

  const handleSearch = () => {
    if (!searchQuery.trim()) {
      setSearchResults([]);
    } else {
      fetch(`${apiBase}/movies/search?q=${encodeURIComponent(searchQuery)}`)
        .then(res => res.json())
        .then(setSearchResults)
        .catch(console.error);
    }
  };

  return (
    <div className="App">
      <header>
        <h1>Movie Recommendations</h1>
        <div className="search-bar">
          <input
            type="text"
            placeholder="Search or type movie name..."
            value={searchQuery}
            onChange={e => setSearchQuery(e.target.value)}
            onKeyDown={e => e.key === "Enter" && handleSearch()}
            style={{width: "300px", padding: "8px", fontSize: "16px", borderRadius: "4px"}}
          />
          <button onClick={handleSearch} style={{padding: "8px 16px", marginLeft: "8px", cursor: "pointer", borderRadius: "4px", backgroundColor: "#e50914", color: "white", border: "none", fontWeight: "bold"}}>Search</button>
        </div>
      </header>

      {searchResults.length > 0 && (
        <div>
          <h2>Search Results</h2>
          <Carousel title="" movies={searchResults} />
        </div>
      )}

      <Carousel title="Popular Movies" movies={popularMovies} />

      {genres.map(genre => (
        <Carousel key={genre} title={genre} movies={genreMovies[genre] || []} />
      ))}
    </div>
  );
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);
