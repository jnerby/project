const ClubButtons = () => {
    const [club_id, updateClub] = React.useState();
    const [buttons, updateButtons] = React.useState([]);

    React.useEffect(() => {
        fetch('/club-buttons')
        .then(response => {
            return response.json();
            })
        .then(clubs => {
            const btns = [];
            // Generate buttons key = club_id, value = club name
            for (const [key, value] of Object.entries(clubs)) {
                btns.push(
                    // Use club_id as button key
                    <div id={`btn_div${key}`}>
                        {/* Button on click updates state to club's id */}
                        <button className="removeBtn btn btn-dark" onClick={() => updateClub(key)}>{value}</button>
                    </div>
                );
            }
            updateButtons(btns);
        });

    }, []);
    return (
        <React.Fragment>
            <section className="word-container watchlist">{buttons}</section>
            <Watchlist club_id={club_id} />
        </React.Fragment>
    )
}

const Watchlist = (props) => {
    const [movies, updateMovies] = React.useState([]);

    // Remove a film from a list
    function removeFilm(evt) {
        const film_id = evt.target.id.slice(3);

        fetch(`/remove-film?id=${film_id}`)
            .then(response => response.text())
            .then(evt.target.disabled = true)
            // .then(result => updateMovies(movies.filter((item) => item.id != `div${film_id}`)))
            // .then(console.log(movies))
    }
    function watchedFilm(evt) {
        const film_id = evt.target.id.slice(2);
        console.log(film_id);
        fetch(`/watched-film?id=${film_id}`)
            .then(response => response.text())
            .then(evt.target.disabled = true)
    }

    React.useEffect(() => {
        fetch(`/watchlist?club_id=${props.club_id}`)
            .then(response => response.json())
            .then(films => {
                // Get values from result dictionary
                const values = Object.values(films);
                // Initiliaze empty helper array for movie details
                const helper = [];
                // Loop over film objects
                for (const [key, value] of Object.entries(films)) {
                    helper.push(
                        <div id={`div${key}`}>
                            <div>
                            <img src={`https://image.tmdb.org/t/p/w500/${value['poster_path']}`}></img>
                            </div>
                            <button id={`rmv${key}`} onClick={removeFilm} className="removeBtn btn btn-dark">Remove</button>
                            <button id={`wt${key}`} onClick={watchedFilm} className="watchBtn btn btn-dark">Watched</button>
                            <h4>{value['title']}</h4>
                            <p>{value['overview']}</p>
                            <p>Voter Average: {value['vote_average']}</p>
                            <p>Runtime: {value['runtime']}</p>
                            <ul>Genres 
                            {value['genres'].map(genre => (<li>{genre['name']}</li>))}
                            </ul>
                        </div>
                    );
                }
                // Replace empty movies array in state with values from helper array
                updateMovies(movies => helper);
                
            })},[props.club_id]);
    return <section className="word-container watchlist">{movies}</section>;
}

ReactDOM.render(<ClubButtons />, document.querySelector('#root'));


// add form to search by genre/runtime