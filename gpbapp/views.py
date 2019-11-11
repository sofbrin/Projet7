from flask import Flask, render_template, request, jsonify
#from dotenv import load_dotenv
import os
from gpbapp.grandpyAnswer import GrandpyAnswer

app = Flask(__name__)
app.config['API_KEY'] = os.getenv('API_KEY')


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
