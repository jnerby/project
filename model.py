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
    user_votes = db.relationship('Film', secondary='votes', back_populates='vote_users')

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
    watched = db.Column(db.Boolean,
                        default=False,
                        nullable=False)

    club = db.relationship('Club', back_populates='films')
    vote_users = db.relationship('User', secondary='votes', back_populates='user_votes')

    def __repr__(self):
        return f"<Film film_id={self.film_id} date_added={self.date_added} watched={self.watched}>"

class Vote(db.Model):
    """User up and downvotes"""

    __tablename__ = 'votes'

    vote_id = db.Column(db.Integer,
                        primary_key=True,
                        autoincrement=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'),
                        nullable=False)
    film_id = db.Column(db.Integer,
                        db.ForeignKey('films.film_id'),
                        nullable=False)
    vote = db.Column(db.Boolean,
                    nullable=False)

    def __repr__(self):
        return f"<Vote vote_id={self.vote_id} vote={self.vote}>"


if __name__ == "__main__":
    from server import app
    connect_to_db(app)