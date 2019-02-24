#!/usr/bin/python3
import os
from pathlib import Path
import random
from string import ascii_letters

from flask import Flask, render_template, request, url_for, redirect, jsonify, send_from_directory
from flask_cors import CORS
import requests
import json

from inspiration_app.models import User, Song, SongTemplate, Key, Tempo, Cluster, songs_liked
from inspiration_app import db, app

import inspiration_engine.data_manipulation as dm
import inspiration_engine.clustering as clustering
from inspiration_engine.myMusicTest import wavListCreator, mergeWavFiles
CORS(app)

basedir = os.path.abspath(os.path.dirname(__file__))
TYPEFORM_KEY = '91a81GGkfUWdBa38YWPG6zygkx4vvKD5eNFpKKcKykFW'
MODEL_FILENAME = '/Users/alanbato/Code/inspiration/inspiration_app/kmeans_model.sav'
URL_WEB = 'https://3183e6e5.ngrok.io'

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Song': Song,
        'SongTemplate': SongTemplate,
        'Key': Key,
        'Tempo': Tempo,
        'Cluster': Cluster
    }


@app.route('/')
def landing():
    response = requests.post(
        'https://api.typeform.com/forms',
        headers={'Authorization': 'Bearer {}'.format(TYPEFORM_KEY)},
        data=json.dumps(
            {
                'title': 'Song Preference Form',
                'settings': {'is_public': True},
                'fields': [
                    {
                        'ref': 'song_url',
                        'title': 'Song 1',
                        'type':'yes_no',
                        'properties': {'description': 'Please listen to https://gcp.com/media/our_file'},
                        'attachment': { "type": "video", "href": "https://www.youtube.com/watch?v=wCrtk-pyP0I"},
                    }
                ]
            }
        )
    )
    
    form_link = response.json()['_links']['display']
    return render_template('index.html', data={'form_url': form_link, 'url_web': URL_WEB})

@app.route('/populate')
def populate_db():
    """Populate the db with the common pop/rock songs file"""

    songs = dm.parse_file('static/common_songs.txt')
    freq_matrix = dm.get_frequency_matrix(songs)
    model, clusters = clustering.clusterize(freq_matrix)
    clustering.save(model, MODEL_FILENAME)
    clusters_for_db = {}
    try:
        for song, cluster_id in zip(songs, clusters):
            if cluster_id in clusters_for_db:
                cluster = clusters_for_db[cluster_id]
            else:
                cluster = Cluster(name=str(cluster_id))
                clusters_for_db[cluster_id] = cluster
                db.session.add(cluster)
            template = SongTemplate(numerals=",".join(song), cluster=cluster)
            db.session.add(template)
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
        return "DB Population Failed"
    else:
        return "DB Populated with {} song(s).".format(len(songs))

@app.route('/like/<username>/<song_id>')
def like_song(username, song_id):
    user = User.query.filter(User.username == username).first()
    song = Song.query.get(int(song_id))
    print('like', user, song)
    try:
        user.liked_songs.append(song)
        db.session.add(user)
        db.session.commit()
        print('song liked')
    except Exception as e:
        print(e)
        db.session.rollback()
    print('User {} now likes {}'.format(username, song_id))
    return redirect(url_for('new_song', user=username))

@app.route('/login/<username>')
def login(username):
    return "Not Implemented"

@app.route('/add/<numerals>')
def add_song_route(numerals):
    return add_song(numerals)

@app.route('/<user>/new')
def new_song(user):
    # Random song
    username = user
    user = User.query.filter(User.username == username).first()
    if not user:
        user = User(username=username)
        db.session.add(user)
        db.session.commit()
        song = random.choice(Song.query.all())
        song_url = song.file_url
        song_id = song.id
    else:
        magic = random.randint(1,4)
        if magic == 1 and user.liked_songs.first() is not None:
            cluster = random.choice(user.liked_songs.all()).template.cluster
            rand_template = random.choice(cluster.templates.all())
            song_url, song_id = make_song_from_numeral(rand_template)
            song_url = '/' + song_url
        elif magic == 2 and user.liked_songs.first() is not None:
            cluster = random.choice(user.liked_songs.all()).template.cluster
            rand_template = random.choice(cluster.templates.all())
            rand_song = random.choice(rand_template.songs.all())
            song_url = rand_song.file_url
            song_id = rand_song.id
        elif magic == 3:
            rand_template = random.choice(SongTemplate.query.all())
            song_url, song_id = make_song_from_numeral(rand_template)
            song_url = '/' + song_url
        else:
            song = random.choice(Song.query.all())
            song_url = song.file_url
            song_id = song.id
    return render_template('song.html', data={'url_file': song_url, 'song_id': song_id, 'user': user.username, 'url_web': URL_WEB})
    
    
@app.route('/new_song/<song_template_id>')
def make_song_route(song_template_id):
    template = SongTemplate.query.get(song_template_id)
    return make_song_from_numeral(template)

def make_song_from_numeral(song_template):
    numerals = song_template.numerals
    numeral_list = dm.parse_song(numerals)
    music_style = song_template.cluster.name
    output_files = ["CS1.wav", "CS2.wav", "CS3.wav", "CS4.wav"]
    #output_files = ["{}".format(filename) for filename in output_files]
    song_name = "".join(random.choices(ascii_letters, k=10))
    final_song_filename = "static/songs/{}.wav".format(song_name)
    print(music_style)
    wavListCreator(numeral_list, output_files, musicSTYLE=music_style)
    mergeWavFiles(output_files, final_song_filename)
    key = Key.query.first()
    tempo = Tempo.query.first()
    try:
        new_song = Song(file_url='/'+final_song_filename, template=song_template, key=key, tempo=tempo)
        db.session.add(new_song)
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
        return "Song creation failed for: {}".format(numerals)
    else:
        return final_song_filename, new_song.id



def add_song(numerals):
    song = dm.parse_song(numerals)
    freq_vector = dm.get_frequency_matrix([song])
    model = clustering.load(MODEL_FILENAME)
    predicted_cluster = int(model.predict(freq_vector)[0])
    print('cluster', predicted_cluster)
    try:
        cluster = Cluster.query.get(predicted_cluster)
        print(cluster)
        template = SongTemplate(numerals=",".join(song), cluster=cluster)
        db.session.add(template)
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
        return "Song insertion failed for: {}".format(numerals)
    else:
        return "Song inserted: {}".format(numerals)