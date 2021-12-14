function Modal(evt) {
    evt.preventDefault();

    // Fetch movie details from server using tmdb_id
    const tmdb_id = evt.target.id; 
    fetch(`/api-details?id=${tmdb_id}`)
    // make AJAX request
        .then(response => response.json())
        // parse response from AJAX request
        .then(movieDetails => {
            // separate movie details from clubs in server's response
            const details = movieDetails['api_result'];
            ///// separate clubs into a second fetch request. add club drop down as adjacentHTML in modal
            const clubs = movieDetails['clubs'];

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
                                <button id="addBtn" type="button" class="btn btn-secondary">Add to List</button>
                                </div>`;

            // make the modal visible
            modal.style.display = "block";

            // get close button for model
            const closeBtn = document.getElementById("close");
            // when close button is clicked, hide the modal
            closeBtn.addEventListener('click', () => modal.style.display="none");

            // get Add to List Button
            const addBtn = document.getElementById("addBtn");
            // when Add to List is clicked, call add_to_list function in server.py
            addBtn.addEventListener('click', (evt) => {
                // get club id
                const club_id = evt.target.name;
                console.log(club_id);
                const data = {
                    tmdb_id: tmdb_id,
                    club_id: club_id
                }
                // send post request
                fetch('/add-to-list', {
                ///// TUESDAY
                // fetch(`/add-to-list?tmdb_id=${tmdb_id}&club_id=${club_id}`, {
                    method: 'POST',
                    body: JSON.stringify(data),
                    headers: {
                        'Content-Type': 'application/json',
                        },
                    })
                    .then(response => response.text())
                    // replace button text
                    .then(result => {
                        addBtn.innerHTML = result;
                    });
            });
        });
}

function Result(props) {
    return (
        <React.Fragment>
            <div className="container-fluid search-result">
                {/* map each result's poster path to image */}
                {props.searchResults.map((result) => (
                    <img className="modal-btn" key={result['id']} id={result['id']} alt={result['title']} 
                    src={'https://image.tmdb.org/t/p/w500/' + result['poster_path']} 
                    onClick={Modal}></img>))}
            </div>
        </React.Fragment>
    ); 
} 

function SearchForm() {
    // use state to store search results from API call
    const [searchResults, updateSearchResults] = React.useState([]);
    // pass search form submission as evt to queryAPI
    function queryAPI(evt){
        evt.preventDefault();
        const userSearch = document.querySelector('#search').value;
        fetch(`/api?search=${userSearch}`)
            // make AJAX request
            .then(response => response.json())
            // parse response from AJAX request
            .then(searchResults => {
                // storing json response at results key in results variable
                const apiResults = searchResults['results'];
                updateSearchResults(apiResults);
            });
    }
    return (
        <React.Fragment>
            <form onSubmit={queryAPI} className="container-fluid text-right" id="search-form">
                <input type="search" placeholder="Title" aria-label="Search" name="search" id="search"></input>
                <button className="btn btn-outline-secondary" type="submit">Search</button>
            </form>
            {/* call RenderResults w/ searchResults state */}
            <Result searchResults={searchResults}/>
        </React.Fragment>
    )
}

ReactDOM.render(<SearchForm />, document.querySelector('#search-form-div'));