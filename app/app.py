#!/usr/bin/python3

from flask import Flask, render_template, request, url_for, redirect, jsonify, send_from_directory
from flask_cors import CORS
import requests
import json
app = Flask(__name__)
CORS(app)
TYPEFORM_KEY = '91a81GGkfUWdBa38YWPG6zygkx4vvKD5eNFpKKcKykFW'

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




if __name__ == '__main__':
    app.run(debug=True, host= '0.0.0.0')