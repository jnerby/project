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
            <SearchList club_id={club_id} />
        </React.Fragment>
    )
}

const Filter = (evt) => {
    // get genre user selected
    const selectedGenre = evt.target.value;

    // get all movie divs
    const divs = document.getElementsByClassName('watchDiv');

    // if selected genre = All Genres, make everything visible
    if (selectedGenre == "All Genres"){
        for (const d of divs){
            d.style.display = "block";
        }
    } else {
        // loop through movie divs
        for (const d of divs){
            const genItems = d.getElementsByClassName('genreItem');
            // get all genres for a movie
            const movieGenres = [];
            for (const g of genItems) {
                movieGenres.push(g.innerHTML);
            }
            // hide movies that do not have selected genre
            if (!movieGenres.includes(selectedGenre)) {
                d.style.display = "none";
            }
            // display all other movies
            else {
                d.style.display = "block";
            } 
        }
    }
} 

const FilterRuntime = (evt) => {
    // get genre user selected
    const selectedRuntime = parseInt(evt.target.value);
    // get all movie divs
    const divs = document.getElementsByClassName('watchDiv');
    // loop through movie dives
    if (selectedRuntime == "All"){
        for (const d of divs){
            d.style.display = "block";
        }
    } else {
        for (const d of divs){
            // get runtime paragraph
            const rt_paragraph = d.querySelector('#runtime').innerHTML;
            // get runtime value from innerHTML
            const film_rt = parseInt(rt_paragraph.slice(9));
            if (selectedRuntime > film_rt) {
                d.style.display = "none";
            }
            // display all other movies
            else {
                d.style.display = "block";
            } 
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
            <section className="word-container">
                <h5>Filters</h5>
                <h6>Genres</h6>
                <p id="selectedGen"></p>
                <form>
                <select onChange={Filter} id="genreSelectEl">
                    {genres.map(genre => (<option value={genre} id={genre}>{genre}</option>))}
                </select>
                </form>
                <br></br>
                <h6>Runtimes</h6>
                <select onChange={FilterRuntime} id="runtimeSelect">
                    <option value="---">---</option>
                    <option value="All">All</option>
                    <option value="90">90</option>
                    <option value="120">120</option>
                    <option value="150">150</option>
                    <option value="180">180</option>
                    <option value="210">210</option>
                    <option value="240">240</option>
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
                            <p id="runtime">Runtime: {value['runtime']}</p>
                            <ul id="genreList">Genres
                                {value['genres'].map(genre => (<li className="genreItem">{genre['name']}</li>))}
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