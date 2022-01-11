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
                    // sum all ratings for a film
                    let ratings_sum = 0;
                    let ave_ratings = 0;
                    let ave_ratings_literal;
                    for (const val of item['db_ratings']) {
                        ratings_sum += val[0]
                    }
                    // get film's ave rating
                    if (item['db_ratings'].length > 0) {
                        ave_ratings = ratings_sum / item['db_ratings'].length;
                        ave_ratings_literal = `Average Rating: ${ave_ratings}`
                    } else {
                        ave_ratings_literal = `No Ratings. Click to rate!`
                    }
                    // Check if user has already reviewed
                    const rated_users = new Set();
                    for (const rat of item['db_ratings']) {
                        rated_users.add(rat[1]);
                    }
                    if (rated_users.has(username)) {
                        newHistory.push(
                            <div className="cont">
                                <div id={`div${item['db_id']}`} name={item['title']} className="card mb-3" style={{ width: '18rem' }}>
                                    <img id={`img${item['db_id']}`} name={item['title']} className="card-img-top" src={`https://image.tmdb.org/t/p/w500/${item['poster_path']}`} alt="Card image cap"></img>
                                    <div class="card-title">
                                        <h6>{ave_ratings_literal}</h6>
                                    </div>
                                    <div class="card-body">
                                        <ul class="list-group list-group-flust">
                                            {item['db_ratings'].map(rating => (<li class="list-group-item">{rating[1]}: {rating[0]}</li>))}
                                        </ul>
                                    </div>
                                </div>
                            </div>
                        );
                    }
                    else {
                        newHistory.push(
                            <div className="cont">
                                <div id={`div${item['db_id']}`} name={item['title']} className="card mb-3" style={{ width: '18rem' }}>
                                    <img onClick={rateFilm} id={`img${item['db_id']}`} name={item['title']} className="card-img-top" src={`https://image.tmdb.org/t/p/w500/${item['poster_path']}`} alt="Card image cap"></img>
                                    <div class="card-title">
                                        <h6>{ave_ratings_literal}</h6>
                                    </div>
                                    <div class="card-body">
                                        <ul class="list-group list-group-flust">
                                            {item['db_ratings'].map(rating => (<li class="list-group-item">{rating[1]}: {rating[0]}</li>))}
                                        </ul>
                                    </div>
                                </div>
                            </div>
                        );
                    }

                }
                updateHistory(newHistory);
            })
    }, []);

    return (
        <React.Fragment>{history}
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
                            <option value="6">6</option>
                            <option value="7">7</option>
                            <option value="8">8</option>
                            <option value="9">9</option>
                            <option value="10">10</option>
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