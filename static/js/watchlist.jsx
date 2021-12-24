const ClubButtons = () => {
    const [club_id, updateClub] = React.useState(0);
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
            {/* <Watchlist club_id={club_id} /> */}
            <SearchList club_id={club_id} />
        </React.Fragment>
    )
}

const Filter = (evt) => {
    // get genre user selected
    const selectedGenre = evt.target.value;
    // get all movie divs
    const divs = document.getElementsByClassName('watchDiv');
    // loop through movie dives
    for (const d of divs){

        // const genList = d.getElementById('genreList');
        const genItems = d.getElementsByClassName('genreItem');
        // get all genres for a movie
        const movieGenres = [];
        for (const g of genItems) {
            movieGenres.push(g.id);
        }
        /// add something to turn off filter
        if (!movieGenres.includes(selectedGenre)) {
            // console.log(d);
            d.style.display = "none";
        }
        else {
            d.style.display = "block";
        } 
    }
} 

const SearchList = (props) => {
    const [genres, updateGenres] = React.useState([]);
    const club_id = props.club_id
    React.useEffect(() => {
        fetch(`/club-filters?id=${club_id}`)
            .then(response => response.json())
            .then(results => {

                updateGenres(results);
            });
    }, [props.club_id]);
    return (
        <React.Fragment>
            {/* <section className="word-container">{genres}</section> */}
            <section className="word-container">
                <select onChange={Filter} value="genreSelect">
                    {genres.map(genre => (<option value={genre}>{genre}</option>))}
                </select>
            </section>
            <Watchlist club_id={club_id}/>
        </React.Fragment>

    )
}

const Watchlist = (props) => {
    const [movies, updateMovies] = React.useState([]);

    React.useEffect(() => {
        fetch(`/watchlist?club_id=${props.club_id}`)
            .then(response => response.json())
            .then(films => {
                // Initiliaze empty helper array for movie details
                const helper = [];
                // Loop over film objects
                for (const [key, value] of Object.entries(films)) {
                    helper.push(
                        <div id={`div${key}`} className="watchDiv">
                            <div>
                                <img id={`img${key}`} name={value['title']} src={`https://image.tmdb.org/t/p/w500/${value['poster_path']}`} onClick={Modal}></img>
                            </div>
                            <h4>{value['title']}</h4>
                            <h5>View Date: {value['view_date']}</h5>
                            <p>{value['overview']}</p>
                            <p>Voter Average: {value['vote_average']}</p>
                            <p>Runtime: {value['runtime']}</p>
                            <ul id="genreList">Genres
                                {value['genres'].map(genre => (<li className="genreItem" id={genre['name']}>{genre['name']}</li>))}
                            </ul>
                        </div>
                    );
                }
                // Replace empty movies array in state with values from helper array
                updateMovies(movies => helper);

            })
    }, [props.club_id]);
    return (
        <React.Fragment>
            <section className="word-container watchlist">{movies}</section>
        </React.Fragment>
    )
}

function Modal(evt) {
    evt.preventDefault();

    const film_id = evt.target.id.slice(3);
    const film_name = evt.target.name;

    const modal = document.getElementById("list-modal");

    // add schedule button if not scheduled
    fetch(`/schedule-check?id=${film_id}`)
        .then(response => response.text())
        .then(scheduled => {
            if (scheduled == 'True') {
                modal.innerHTML = `<div class=modal-content><span id="close" align="right" class=close>&times;</span>
                                <h1>${film_name}</h1>
                                <button id="rmv${film_id}" class="removeBtn btn btn-dark">Remove</button>
                                <br>
                                <button id="wt${film_id}" class="watchBtn btn btn-dark">Watched</button> 
                                <br>
                                </div>`;

                // make the modal visible
                modal.style.display = "block";

                // get close button for model
                const closeBtn = document.getElementById("close");
                // when close button is clicked, hide the modal
                closeBtn.addEventListener('click', () => modal.style.display = "none");

                // Remove from List
                const rmv = modal.querySelector('.removeBtn');

                rmv.addEventListener('click', (evt) => {
                    const film_id = evt.target.id.slice(3);

                    fetch(`/remove-film?id=${film_id}`)
                        .then(response => response.text())
                        .then(evt.target.disabled = true)
                });

                // Mark as watched
                const wat = modal.querySelector('.watchBtn');

                wat.addEventListener('click', (evt) => {
                    const film_id = evt.target.id.slice(2);

                    fetch(`/watched-film?id=${film_id}`)
                        .then(response => response.text())
                        .then(evt.target.disabled = true)
                })

            }
            else {
                modal.innerHTML = `<div class=modal-content><span id="close" align="right" class=close>&times;</span>
                                <h1>${film_name}</h1>
                                <button id="rmv${film_id}" class="removeBtn btn btn-dark">Remove</button>
                                <br>
                                <button id="wt${film_id}" class="watchBtn btn btn-dark">Watched</button> 
                                <br>
                                <input type="date" id="schedDate">
                                <button id="sch${film_id}" class="schBtn btn btn-dark">Schedule</button> 
                                </div>`;

                // make the modal visible
                modal.style.display = "block";

                // get close button for model
                const closeBtn = document.getElementById("close");
                // when close button is clicked, hide the modal
                closeBtn.addEventListener('click', () => modal.style.display = "none");

                // Remove from List
                const rmv = modal.querySelector('.removeBtn');

                rmv.addEventListener('click', (evt) => {
                    const film_id = evt.target.id.slice(3);

                    fetch(`/remove-film?id=${film_id}`)
                        .then(response => response.text())
                        .then(evt.target.disabled = true)
                });

                // Mark as watched
                const wat = modal.querySelector('.watchBtn');

                wat.addEventListener('click', (evt) => {
                    const film_id = evt.target.id.slice(2);
                    fetch(`/watched-film?id=${film_id}`)
                        .then(response => response.text())
                        .then(evt.target.disabled = true)
                })

                // Schedule
                const sched = modal.querySelector('.schBtn')

                sched.addEventListener('click', (evt) => {
                    const dt = document.querySelector('#schedDate').value;
                    const film_id = evt.target.id.slice(3);
                    fetch(`/schedule?id=${film_id}&date=${dt}`)
                        .then(response => response.text())
                        .then(evt.target.disabled = true)
                })
            }
        })
}

ReactDOM.render(<ClubButtons />, document.querySelector('#root'));