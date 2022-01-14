DESCRIPTION
watchList allows users to start or join film clubs and collaboratively build a club's watchList. This project differs from IMdB and Letterboxd's lists by allowing users to create and share with others. watchList takes care of everything a film club needs to collaborate! Club members can schedule viewings, rate films, and receive custom recommendations based on their viewing history and ratings. The homepage allows users to filter a watchlist by genre and max runtime to help them decide which film to watch. Users can also sign up to receive text message notifications when a viewing is scheduled or canceled.

TECH STACK
Languages: Python, Javascript, HTML, CSS
Database: PostgreSQL
Frameworks & Libraries: Flask, React, Jinja, Boostrap
APIs: TMDB, Twilio

	This app uses React to render the following pages the home page, Upcoming, and Log. All film data and artwork come from TMDB’s API. This app uses Twilio to send messages to club members when a film viewing is scheduled or a scheduled viewing is canceled.

FEATURES
Home page
![alt text](https://github.com/jnerby/watchlist/static/images/twilio.jpg)
The home page shows a user’s clubs and saved films. When a user clicks on a film’s cover art, a modal window appears so a user can remove the film, mark the film as watched, or schedule a date to watch it. Users can turn notifications on and off and review join requests for their clubs. When a user has their notifications turned on, they receive text messages whenever another club member schedules or cancels a film viewing.



Recommendations

watchList’s search page is populated with recommendations based on a user’s film ratings. 

INSTALL
