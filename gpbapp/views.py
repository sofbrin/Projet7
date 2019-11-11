from flask import Flask, render_template, request, jsonify
import os
from gpbapp.grandpyAnswer import GrandpyAnswer
from settings import API_KEY

app = Flask(__name__)
app.config['API_KEY'] = API_KEY


@app.route('/')
@app.route('/index/')
def index():
    return render_template('index.html')


@app.route('/grandpyAnswer/', methods=['POST'])
def get_answer():
    data = request.get_json()
    grandpy = GrandpyAnswer(data['question'])
    result = grandpy.gpbAnswer()
    return jsonify(result)
