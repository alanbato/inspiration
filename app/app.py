#!/usr/bin/python3

from flask import Flask, render_template, request, url_for, redirect, jsonify, send_from_directory

app = Flask(__name__)

TYPEFORM_KEY = '91a81GGkfUWdBa38YWPG6zygkx4vvKD5eNFpKKcKykFW'

@app.route('/')
def landing():
    return render_template('index.html')




if __name__ == '__main__':
    app.run(debug=True, host= '0.0.0.0')