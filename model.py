from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_to_db(flask_app, db_uri="postgresql:///watchlist", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = False
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")

class User(db.Model):
    """A user"""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer,
                        primary_key=True,
                        autoincrement=True)
    fname = db.Column(db.String(25))
    lname = db.Column(db.String(25))
    email = db.Column(db.String(30))
    username = db.Column(db.String(25),
                        unique=True)
    password_hash = db.Column(db.String(128))

    clubs = db.relationship('Club', secondary='club_users', back_populates='users')
    user_ratings = db.relationship('Film', secondary='ratings', back_populates='ratings_users')

    def __repr__(self):
        return f"<User user_id={self.user_id} username={self.username}>"

class ClubUser(db.Model):
    """User-club association"""

    __tablename__ = 'club_users'

    club_user_id = db.Column(db.Integer,
                        primary_key=True,
                        autoincrement=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'),
                        nullable=False)
    club_id = db.Column(db.Integer,
                        db.ForeignKey('clubs.club_id'),
                        nullable=False)
    approved = db.Column(db.Boolean,
                        default=False,
                        nullable=False)
    
    def __repr__(self):
        return f"<ClubUser user_id={self.user_id} club_id={self.club_id} approved={self.approved}>"

class Club(db.Model):
    """A Club"""

    __tablename__ = 'clubs'

    club_id = db.Column(db.Integer,
                        primary_key=True,
                        autoincrement=True)
    name = db.Column(db.String(30))
    owner_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'))

    users = db.relationship('User', secondary='club_users', back_populates='clubs')
    films = db.relationship('Film', back_populates='club')

    def __repr__(self):
        return f"<Club club={self.name} owner={self.owner_id}>"

class Film(db.Model):
    """A film"""

    __tablename__ = 'films'

    film_id = db.Column(db.Integer,
                        primary_key=True,
                        autoincrement=True)
    club_id = db.Column(db.Integer,
                        db.ForeignKey('clubs.club_id'),
                        nullable=False)
    tmdb_id = db.Column(db.Integer)
    date_added = db.Column(db.DateTime)
    added_by = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'),
                        nullable=False)
    view_schedule = db.Column(db.DateTime)
    watched = db.Column(db.Boolean,
                        default=False,
                        nullable=False)

    club = db.relationship('Club', back_populates='films')
    ratings_users = db.relationship('User', secondary='ratings', back_populates='user_ratings')

    def __repr__(self):
        return f"<Film film_id={self.film_id} date_added={self.date_added} watched={self.watched}>"


#### NEED USER_RATINGS TABLE
class Rating(db.Model):
    """User ratings"""

    __tablename__ = 'ratings'

    rating_id = db.Column(db.Integer,
                        primary_key=True,
                        autoincrement=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'),
                        nullable=False)
    film_id = db.Column(db.Integer,
                        db.ForeignKey('films.film_id'),
                        nullable=False)
    rating = db.Column(db.Integer,
                    nullable=False)

    def __repr__(self):
        return f"<Rating rating_id={self.rating_id} rating={self.rating}>"


if __name__ == "__main__":
    from server import app
    connect_to_db(app)