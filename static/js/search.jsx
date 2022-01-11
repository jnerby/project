function SearchForm() {
    // QUERY API WHEN USER SEARCHES FOR A TITLE
    document.getElementById('body').innerHTML = "";
    // use state to store search results from API call
    const [searchResults, updateSearchResults] = React.useState([]);
    // pass search form submission as evt to queryAPI
    function queryAPI(evt) {
        evt.preventDefault();
        const userSearch = document.querySelector('#search').value;
        document.getElementById('recs').innerHTML = "";
        fetch(`/api?search=${userSearch}`)
            // make AJAX request
            .then(response => response.json())
            // parse response from AJAX request
            .then(apiResults => {
                // storing json response at results key in results variable
                updateSearchResults(apiResults);
            });
    }
    return (
        <React.Fragment>
            <form onSubmit={queryAPI} className="container-fluid text-right topcorner" id="search-form">
                <input type="search" size="100" className="form-control" placeholder="Title" aria-label="Search" name="search" id="search"></input>
                <button className="btn btn-outline-secondary" type="submit">Search</button>
            </form>
            {/* call Result w/ searchResults state as prop */}
            <Result searchResults={searchResults} />
        </React.Fragment>
    )
}

function Result(props) {
    // DISPLAY MOVIE POSTERS FROM SEARCH RESULT
    return (
        <React.Fragment>
            <div className="container-fluid search-result">
                {props.searchResults.map((result) => {
                    if (result['db_status']) {
                        return (
                                <div className="cont">
                                <h1 className="text-block">{result['db_status']}</h1>
                                <img className="modal-btn gray-img" key={result['id']} id={result['id']} alt={result['db-status']} 
                                src={'https://image.tmdb.org/t/p/w500/' + result['poster_path']} 
                                onClick={Modal}></img>
                                </div>
                        );
                    }
                    else {
                        return (
                            <img className="modal-btn" key={result['id']} id={result['id']} alt={result['db-status']}
                                src={'https://image.tmdb.org/t/p/w500/' + result['poster_path']}
                                onClick={Modal}></img>
                        );
                    }
                })
            }
            </div>
        </React.Fragment>
    );
}

function Modal(evt) {
    // RENDER MODAL WHEN USER CLICKS ON A MOVIE POSTER
    evt.preventDefault();
    // Fetch movie details from server using tmdb_id
    const tmdb_id = evt.target.id;
    fetch(`/api-details?id=${tmdb_id}`)
        // make AJAX request
        .then(response => response.json())
        // parse response from AJAX request
        .then(movieDetails => {
            // separate movie details from clubs in server's response
            const details = movieDetails;
            // assign variables to use in modal
            const title = details['title'];
            const overview = details['overview'];
            const lang = details['original_language'];
            const vote_ave = details['vote_average'];
            const runtime = details['runtime'];
            const release = details['release_date'];

            // get the modal element
            const modal = document.getElementById("myModal");
            // set innerHMTL to modal-content class
            modal.innerHTML = `<div class=modal-content><span id="close" align="right" class=close>&times;</span>
                                    <h1>${title}</h1>
                                    <p>Overview: ${overview}</p>
                                    <p>Runtime: ${runtime}</p>
                                    <p>Average Vote: ${vote_ave}</p>
                                    <p>Release Date: ${release}</p>
                                    <label>Club</label><select class="btn btn-secondary dropdown-toggle" id="club-dropdown"></select>
                                    <br>
                                    <button id="addBtn" type="button" class="btn btn-dark">Add to List</button>
                                    </div>`;

            // make the modal visible
            modal.style.display = "block";

            // get close button for model
            const closeBtn = document.getElementById("close");
            // when close button is clicked, hide the modal
            closeBtn.addEventListener('click', () => modal.style.display = "none");

            // get clubDropdown element for modal
            const clubDropdown = document.getElementById('club-dropdown');

            // fetch names of user's clubs from server so user can select which list to add to
            fetch('/club-names')
                .then(response => response.json())
                .then(clubs => {
                    // loop through clubs add add name and id to options in dd
                    for (const [key, value] of Object.entries(clubs)) {
                        const opt = document.createElement("option");
                        opt.innerHTML = key;
                        opt.value = value;
                        clubDropdown.appendChild(opt);
                    }
                });

            // get Add to List Button
            const addBtn = document.getElementById("addBtn");

            // when Add to List is clicked, call add_to_list function in server.py
            addBtn.addEventListener('click', (evt) => {
                // get club_id from dropdown
                const club_id = clubDropdown.options[clubDropdown.selectedIndex].value;
                fetch(`/add-to-list?tmdb_id=${tmdb_id}&club_id=${club_id}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                })
                    .then(response => response.text())
                    // replace button text
                    .then(result => {
                        addBtn.innerHTML = result;
                        modal.style.display = "none"
                    });
            });
        });
}

ReactDOM.render(<SearchForm />, document.querySelector('#search-form-div'));