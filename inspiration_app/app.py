#!/usr/bin/python3
import os
from pathlib import Path
import random
from string import ascii_letters

from flask import Flask, render_template, request, url_for, redirect, jsonify, send_from_directory
from flask_cors import CORS
import requests
import json

from inspiration_app.models import User, Song, SongTemplate, Key, Tempo, Cluster
from inspiration_app import db, app

import inspiration_engine.data_manipulation as dm
import inspiration_engine.clustering as clustering
CORS(app)

basedir = os.path.abspath(os.path.dirname(__file__))
TYPEFORM_KEY = '91a81GGkfUWdBa38YWPG6zygkx4vvKD5eNFpKKcKykFW'
MODEL_FILENAME = '/Users/alanbato/Code/inspiration/inspiration_app/kmeans_model.sav'


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
    return render_template('index.html', data={'form_url': form_link})

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

@app.route('/add/<numerals>')
def add_song_route(numerals):
    return add_song(numerals)

@app.route('/<user>/new')
def new_song(user):
    pass

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