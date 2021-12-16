// get all club buttons
const clubs = document.getElementsByClassName('club-list');
// add event listener to each club button to pass club_id to Watchlist
for (const club of clubs){
        club.addEventListener('click', (evt) =>{
            evt.preventDefault();
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
                            <img src={`https://image.tmdb.org/t/p/w500/${value['poster_path']}`}></img>
                            <p>{value['title']}</p>
                            <p>{value['overview']}</p>
                            <p>Voter Average: {value['vote_average']}</p>
                            <p>Runtime: {value['runtime']}</p>
                        </div>
                        );
                }
                // replace empty movies array in state with values from helper array
                updateMovies(helper);
            })},[props.club_id]);

    return <section className="word-container search-result">{movies}</section>;
}




// const clubs = document.getElementsByClassName('club-list');
// // add event listener for each club name button
// for (const club of clubs){
//     club.addEventListener('click', (evt) =>{
//         evt.preventDefault();
//         // get club_id
//         const club_id = evt.target.id;
//         // fetch club's watch list from server
//         fetch(`/watchlist?club_id=${club_id}`)
//         .then(response => response.json())
//         .then(result => {
//             console.log(result);
//             const films = result;
//             const values = Object.values(films);
//             for (const [key, value] of Object.entries(films)) {
//                 // create div for each film
//                 const filmDiv = document.createElement('div');

//                 // create poster elemnt and append to div
//                 const filmPoster = document.createElement('img');
//                 filmPoster.src = `https://image.tmdb.org/t/p/w500/${value['poster_path']}`;
//                 filmDiv.appendChild(filmPoster);

//                 // create title element and append to filmDiv
//                 const filmTitle = document.createElement('h1');
//                 filmTitle.innerHTML = value['title'];
//                 filmDiv.appendChild(filmTitle);

//                 // create overview element and append to filmDiv
//                 const filmOverview = document.createElement('p');
//                 filmOverview.innerHTML = value['overview'];
//                 filmDiv.appendChild(filmOverview);

//                 // create voter average element and append to filmDiv
//                 const filmVoteAve = document.createElement('p');
//                 filmVoteAve.innerHTML = `Voter Average: ${value['vote_average']}`;
//                 filmDiv.appendChild(filmVoteAve);

//                 // create film runtime element and append to filmDiv
//                 const filmRuntime = document.createElement('p');
//                 filmRuntime.innerHTML = `Runtime: ${value['runtime']}`;
//                 filmDiv.appendChild(filmRuntime);
                
//                 // insert filmDiv at end of of root element
//                 // document.querySelector('#root').insertAdjacentElement('beforeend', filmDiv);
//             }
            
//         });
//     });
// }