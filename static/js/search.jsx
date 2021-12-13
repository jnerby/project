function RenderResults(props) {
    return (
        <React.Fragment>
            <div className="container-fluid search-result">
                {/* map each result's poster path to image */}
                {props.searchResults.map((result) => (
                    <img id={result['id']} alt={result['title']} src={'https://image.tmdb.org/t/p/w500/' + result['poster_path']}></img>))}
            {/* add modal functionality - add on click to each result evt.target to get event that was clicked on */}
            </div>
        </React.Fragment>
    ); 
} 

// function ResultDetails(props) {

// }


function SearchForm() {
    const [searchResults, updateSearchResults ] = React.useState([]);

    function queryAPI(evt){
        evt.preventDefault();

        const userSearch = document.querySelector('#search').value;

        fetch('/api', {

        })
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
            <RenderResults searchResults={searchResults}/>
        </React.Fragment>
    )
}

ReactDOM.render(<SearchForm />, document.querySelector('#search-form-div'));