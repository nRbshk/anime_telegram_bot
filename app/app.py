from flask import Flask, request
from flask_cors import  CORS
from BD import bd
app = Flask(__name__)

CORS(app)

@app.route('/')
def root():
    return "Hello from root"


@app.route('/add_to_list', methods=['POST'])
def add_to_list():
    if request.method == 'POST':
        data = request.json
        resp_message = ""
        try:
            result = bd.save_anime(data['idt'], data['name'].replace("_", " "), data['status'], data['episode'], data['dub_or_sub'], data['page'])
            if result == 2:
                resp_message = "W:Anime is already in list."
            elif result == 1:
                resp_message = "E:Error was occured when inserting in BD."
            else:
                resp_message = "I:OK"
        except:
            resp_message = "E:Error was occured when getting json data."
        return resp_message


@app.route('/set_episode', methods=['POST'])
def set_episode():
    if request.method == 'POST':
        data = request.json
        resp_message = ""
        try:
            bd.set_episode(data['idt'], data['name'].replace("_", " "), data['episode'])
            resp_message = 'I:OK.'
        except:
            resp_message = "E:Error was occured when getting json data"
        return resp_message


def start():
    app.run()

