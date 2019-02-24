from inspiration_app import db

songs_liked = db.Table(
    'songsliked',
    db.Column('user', db.Integer, db.ForeignKey('user.id')),
    db.Column('song', db.Integer, db.ForeignKey('song.id'))
)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    liked_songs = db.relationship(
        'Song',
        secondary=songs_liked,
        backref=db.backref('liked_by', lazy='dynamic'),
        lazy='dynamic',
    )

    def __repr__(self):
        return '<{} {}>'.format(type(self).__name__, self.username)

class Song(db.Model):
    __tablename__ = 'song'
    id = db.Column(db.Integer, primary_key=True)
    file_url = db.Column(db.String(256), unique=True)
    template_id = db.Column(db.Integer, db.ForeignKey('template.id'))
    tempo_id = db.Column(db.Integer, db.ForeignKey('tempo.id'))
    key_id = db.Column(db.Integer, db.ForeignKey('key.id'))
    
    def __repr__(self):
        return '<{} {}>'.format(type(self).__name__, self.file_url)

class Key(db.Model):
    __tablename__ = 'key'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(4))
    songs = db.relationship('Song', backref='key', lazy='dynamic')

    def __repr__(self):
        return '<{} {}>'.format(type(self).__name__, self.name)

class Tempo(db.Model):
    __tablename__ = 'tempo'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(4))
    songs = db.relationship('Song', backref='tempo', lazy='dynamic')

    def __repr__(self):
        return '<{} {}>'.format(type(self).__name__, self.name)

class SongTemplate(db.Model):
    __tablename__ = 'template'
    id = db.Column(db.Integer, primary_key=True)
    numerals = db.Column(db.String(64))
    cluster_id = db.Column(db.Integer, db.ForeignKey('cluster.id'))
    songs = db.relationship('Song', backref='template', lazy='dynamic')

    def __repr__(self):
        return '<{} {}>'.format(type(self).__name__, self.numerals)

class Cluster(db.Model):
    __tablename__ = 'cluster'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    templates = db.relationship('SongTemplate', backref='cluster', lazy='dynamic')

    def __repr__(self):
        return '<{} {}>'.format(type(self).__name__, self.name)