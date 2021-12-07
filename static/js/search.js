document.querySelector('#search-form').addEventListener('submit', (evt) => {
    evt.preventDefault();
    populateSearch();
});

function populateSearch() {     
    // get user search from navbar
    const userSearch = document.querySelector('#search').value;

    // GET AUTH KEY LATER
    const key = '4d17c959fd45a7a8dd63b15b55720251';
    const url = 'https://api.themoviedb.org/3/search/movie?api_key=';

    // send post request to search route w/ value of user_search
    fetch(url+key+'&query='+userSearch, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    })
        // make AJAX request
        .then(response => response.json())
        // parse response from AJAX request
        .then(searchResults => {
            // storing json response at results key in results variable
            const apiResults = searchResults['results'];
            
            // remove all elements from last search
            const body = document.querySelector('body');
            const lastSearch = document.getElementsByClassName('search-result');

            while(lastSearch[0]) {
                lastSearch[0].parentNode.removeChild(lastSearch[0]);
            }

            // add divs for new search results
            for (item of apiResults){
                // create document elements
                const tempDiv = document.createElement('div');
                tempDiv.classList.add('container-fluid');
                tempDiv.classList.add('search-result');
                const tempImage = document.createElement("img");
                tempImage.src = `https://image.tmdb.org/t/p/w500/${item['poster_path']}`;
                tempDiv.appendChild(tempImage);
                body.appendChild(tempDiv);
                    //     <img src="https://image.tmdb.org/t/p/w500/${item['poster_path']}">
                    //     ${item['title']} - ${item['vote_average']} 
                    // </div>`);
            }
        });
}
