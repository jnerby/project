const History = () => {
    const [history, updateHistory] = React.useState([]);
    // Get logged in user's username from h1 in history.html
    const username = document.querySelector('h1').id;

    React.useEffect(() => {
        fetch('/history', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        })
            .then(response => response.json())
            .then(result => {
                const newHistory = [];
                for (const item of result) {
                    // console.log(item['db_ratings']);
                    // if (item.hasOwnProperty('db_ratings')){
                    // sum all ratings for a film
                    let ratings_sum = 0;
                    let ave_ratings = 0;
                    for (const val of item['db_ratings']) {
                        ratings_sum += val[0]
                    }
                    // get film's ave rating
                    if (item['db_ratings'].length > 0) {
                        ave_ratings = ratings_sum / item['db_ratings'].length;
                    }
                    // Check if user has already reviewed
                    const rated_users = new Set();
                    for (const rat of item['db_ratings']) {
                        // console.log(rat[1]);
                        rated_users.add(rat[1]);
                    }
                    // console.log(rated_users);
                    if (rated_users.has(username)) {
                        newHistory.push(
                            <div className="card-group">
                                <div id={`div${item['db_id']}`} className="card" style={{ width: '18rem' }}>
                                    <img id={`img${item['db_id']}`} name={item['title']} className="card-img-top" src={`https://image.tmdb.org/t/p/w500/${item['poster_path']}`} alt="Card image cap"></img>
                                    <div className="card-body">
                                        <p>Average Rating: {ave_ratings}</p>
                                        {item['db_ratings'].map(rating => (<p>{rating[1]}: {rating[0]}</p>))}
                                    </div>
                                </div>
                            </div>
                        );
                    }
                    else {
                        newHistory.push(
                            <div className="card-group">
                                <div id={`div${item['db_id']}`} className="card" style={{ width: '18rem' }}>
                                    <img onClick={rateFilm} id={`img${item['db_id']}`} name={item['title']} className="card-img-top" src={`https://image.tmdb.org/t/p/w500/${item['poster_path']}`} alt="Card image cap"></img>
                                    <div className="card-body">
                                        <p>Average Rating: {ave_ratings}</p>
                                        {item['db_ratings'].map(rating => (<p>{rating[1]}: {rating[0]}</p>))}
                                    </div>
                                </div>
                            </div>
                        );
                    }

                }
                // else {
                //     newHistory.push(
                //         <div id={`div${item['db_id']}`} className="card" style={{ width: '18rem' }}>
                //             <img onClick={rateFilm} id={`img${item['db_id']}`} name={item['title']} className="card-img-top" src={`https://image.tmdb.org/t/p/w500/${item['poster_path']}`} alt="Card image cap"></img>
                //             <div className="card-body">
                //             </div>
                //         </div>
                //     );
                // }
                // }
                updateHistory(newHistory);

            })
    }, []);

    return (
        <React.Fragment>
            <div><section className="word-container">{history}</section></div>
        </React.Fragment>
    );
}

function rateFilm(evt) {
    evt.preventDefault();

    const film_id = evt.target.id.slice(3);

    const modal = document.getElementById("list-modal");

    modal.innerHTML = `<div class=modal-content><span id="close" align="right" class=close>&times;</span>
                        <h1>${evt.target.name}</h1>
                        <label>Rate</label>
                        <select name="rating" id="ratingDD">
                            <option value="1">1</option>
                            <option value="2">2</option>
                            <option value="3">3</option>
                            <option value="4">4</option>
                            <option value="5">5</option>
                        </select>
                        <button id="submitRatingBtn" class="btn btn-dark">Rate</button>
                        </div>`;

    // make the modal visible
    modal.style.display = "block";

    // get close button for model
    const closeBtn = document.getElementById("close");
    // when close button is clicked, hide the modal
    closeBtn.addEventListener('click', () => modal.style.display = "none");

    const submitBtn = document.getElementById('submitRatingBtn');

    submitBtn.addEventListener('click', () => {
        const ratingDropdown = document.getElementById('ratingDD');
        const rating = ratingDropdown.options[ratingDropdown.selectedIndex].value;

        modal.style.display = "none"


        const queryString = new URLSearchParams({ 'film_id': film_id, 'rating': rating }).toString();
        const url = `/rate?${queryString}`;
        fetch(url)
            // make AJAX request
            .then(response => response.text())
            // parse response from AJAX request
            .then(rat => rat)
    })
}
ReactDOM.render(<History />, document.querySelector('#root'));