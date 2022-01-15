## DESCRIPTION
watchList allows users to start or join film clubs and collaboratively build a club's watchList. This project differs from IMdB and Letterboxd's lists by allowing users to create and share with others. watchList takes care of everything a film club needs to collaborate! Club members can schedule viewings, rate films, and receive custom recommendations based on their viewing history and ratings. The homepage allows users to filter a watchlist by genre and max runtime to help them decide which film to watch. Users can also sign up to receive text message notifications when a viewing is scheduled or canceled.

## TECH STACK
Languages: Python, Javascript, HTML, CSS
Database: PostgreSQL
Frameworks & Libraries: Flask, React, Jinja, Boostrap
APIs: TMDB, Twilio

This app uses React to render the following pages the home page, Upcoming, and Log. All film data and artwork come from TMDB’s API. This app uses Twilio to send messages to club members when a film viewing is scheduled or a scheduled viewing is canceled.

## FEATURES
### Home page
![Recs](/static/images/home.png)
The home page shows a user’s clubs and saved films. When a user clicks on a film’s cover art, a modal window appears so a user can remove the film, mark the film as watched, or schedule a date to watch it. Users can turn notifications on and off and review join requests for their clubs.

### Recommendations
![Recs](/static/images/recs.png)
watchList’s search page is populated with recommendations based on a user’s film ratings. 

### Search
![Search](/static/images/search.png)
The search page indicates which search results a user has already watched or saved to a club's watchlist.

### Add to a List
![Add](/static/images/search-modal.png)
When a user clicks on a search result, a modal window opens with additional details about the film. The user can select a club from a dropdown and add the film to the club's list.

## INSTALL
- Install homebrew
- Install git
- In VS Code, run "git clone https://github.com/jnerby/watchlist"
- Cd into the watchlist directory
- Run "pip3 install -r requirements.txt"
- Add a new file to your cloned directory called "secrets.sh"
- Follow these instructions to set up a TMDB API key [TMDB API] (https://developers.themoviedb.org/3/getting-started/authentication). Save your key to secrets.sh by adding this line of code: export API_KEY="KEY". Paste your TMDB API key in quotations after the "="
- Run "source secrets.sh"
- Run "python3 server.py" to launch the app in your browser