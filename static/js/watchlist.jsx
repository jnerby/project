//// CLUB BUTTONS ////
// get all club buttons
const clubs = document.getElementsByClassName('club-list');
// add event listener to each club button to pass club_id to Watchlist
for (const club of clubs){
    club.addEventListener('click', (evt) =>{
        evt.preventDefault();
        // update page header to show which club user is viewing
        document.getElementById('user-lists').innerHTML = evt.target.innerHTML;
        ReactDOM.render(<Watchlist club_id={evt.target.id} />, document.querySelector('#root'));
    });
}


const Watchlist = (props) => {
    const [movies, updateMovies] = React.useState([]);
    React.useEffect(() => {
        fetch(`/watchlist?club_id=${props.club_id}`)
            .then(response => response.json())
            .then(films => {
                // get values from result dictionary
                const values = Object.values(films);
                // initiliaze empty helper array for movie details
                const helper = [];
                // loop over film objects
                for (const [key, value] of Object.entries(films)) {
                    helper.push(
                        <div>
                            <div>
                            <img src={`https://image.tmdb.org/t/p/w500/${value['poster_path']}`}></img>
                            </div>
                            <button id={key} type="button" className="removeBtn btn btn-dark">Remove</button>
                            {/* <button id="addBtn" type="button" class="btn btn-dark">Schedule</button> */}
                            <h4>{value['title']}</h4>
                            <p>{value['overview']}</p>
                            <p>Voter Average: {value['vote_average']}</p>
                            <p>Runtime: {value['runtime']}</p>
                        </div>
                        );
                }
                
                // replace empty movies array in state with values from helper array
                updateMovies(helper);
            })},[props.club_id]);

    return <section className="word-container watchlist">{movies}</section>;
}


// //// REMOVE BUTTONS ////
// // get all remove buttons
// const removeBtns = document.getElementsByClassName('removeBtn');
// // add event listener for when remove button is clicked
// for (const b of removeBtns) {
//     b.addEventListener('click', (evt) =>{
//         evt.preventDefault();
//         console.log(evt.target.id);
//     });
// }
