
    // function rateFilm(evt) {
    //     evt.preventDefault();

    //     const film_id = evt.target.id.slice(2);

    //     const modal = document.getElementById("list-modal");

    //     modal.innerHTML = `<div class=modal-content><span id="close" align="right" class=close>&times;</span>
    //                         <h1>${evt.target.name}</h1>
    //                         <label>Rate</label>
    //                         <select name="rating" id="ratingDD">
    //                           <option value="1">1</option>
    //                           <option value="2">2</option>
    //                           <option value="3">3</option>
    //                           <option value="4">4</option>
    //                         </select>
    //                         <button id="submitRatingBtn" type="submit" class="btn btn-dark">Rate</button>
    //                         </div>`;

    //     // make the modal visible
    //     modal.style.display = "block";

    //     // get close button for model
    //     const closeBtn = document.getElementById("close");
    //     // when close button is clicked, hide the modal
    //     closeBtn.addEventListener('click', () => modal.style.display = "none");

    //     ///////////////
    //     const submitBtn = document.getElementById('submitRatingBtn');
    //     submitBtn.addEventListener('submit', () => {
    //         const ratingDropdown = document.getElementById('ratingDD');
    //         const rating = ratingDropdown.options[ratingDropdown.selectedIndex].value;    
    //         // console.log(rating);
    //         const queryString = new URLSearchParams({'film_id': film_id, 'rating': rating}).toString();
    //         const url = `/rate?${queryString}`;
    //         fetch(url)
    //             // make AJAX request
    //             .then(response => response.text())
    //             // parse response from AJAX request
    //             .then(rat => rat)
    //     })
    // }
