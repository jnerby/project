function RenderModal(evt) {
    evt.preventDefault();
    // const id = evt.target.id; 

    // get the modal element
    const modal = document.getElementById("myModal");    
    // set innerHMTL to modal-content class
    modal.innerHTML = `<div class=modal-content><span id="close" class=close>&times;</span><p>${evt.target.id}</p></div>`;
    // make the modal visibl
    modal.style.display = "block";

    // get close button for model
    const close = document.getElementById("close");
    // when close button is clicked, hide the modal
    close.addEventListener('click', () => modal.style.display="none");
}

function RenderResults(props) {
    return (
        <React.Fragment>
            <div className="container-fluid search-result">
                {/* map each result's poster path to image */}
                {props.searchResults.map((result) => (
                    <img className="modal-btn" key={result['id']} id={result['id']} alt={result['title']} 
                    src={'https://image.tmdb.org/t/p/w500/' + result['poster_path']} 
                    onClick={RenderModal}></img>))}
            </div>
        </React.Fragment>
    ); 
} 

function SearchForm() {
    const [searchResults, updateSearchResults ] = React.useState([]);
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
            <RenderResults searchResults={searchResults}/>
        </React.Fragment>
    )
}

ReactDOM.render(<SearchForm />, document.querySelector('#search-form-div'));
// ReactDom.render(<RenderModal />, document.querySelector('#search-form-div'));