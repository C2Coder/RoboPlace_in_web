#!/bin/python3

from flask import Flask, request
from flask_cors import CORS
import pickle
from threading import Thread
import time

pixels = [[0 for i in range(100)] for j in range(100)]



def save_to_file():
    global pixels
    with open('save.txt', 'wb') as f:
        pickle.dump(pixels, f)

def load_from_file():
    global pixels
    with open('save.txt', 'rb') as f:
        pixels = pickle.load(f)

load_from_file()

def background_task():
    while True:
        #print('saved')
        save_to_file()
        time.sleep(60)

chars = ["a", "b", "c", "d", "e", "f", "g", "h",
         "i", "j", "k", "l", "m", "n", "o", "p",]


colors = ['white', 'platinum', 'grey', 'black', 'pink', 'red', 'orange',
          'brown', 'yellow', 'lime', 'green', 'cyan', 'lblue', 'blue', 'mauve', 'purple']

hex_colors = ['#FFFFFF', '#E4E4E4', '#888888', '#222222', '#FFA7D1', '#E50000', '#E59500',
              '#A06A42', '#E5D900', '#94E044', '#02BE01', '#00D3DD', '#0083C7', '#0000EA', '#CF6EE4', '#820080']

app = Flask(__name__)
CORS(app)

# main page

@app.route('/', methods=['GET'])
def main_page_response():
    with open("static/index.htm") as index_file:
        return index_file.read()


# request handlers

@app.route('/get_pixels', methods=['GET'])
def handle_request():
    if request.method == 'GET':
        args = dict(request.args)
        #print(dict(args))
        section = args["section"]
        ranges = [[0, 20], [20, 40], [40, 60], [60, 80], [80, 100]]
        response = ""
        for y in range(ranges[int(section)][0], ranges[int(section)][1]):
            for x in range(100):
                response = response + str(chars[pixels[x][y]])
            response = response
        return response


@app.route('/post', methods=['POST'])
def handle_incoming():
    global pixels
    if request.method == 'POST':
        # Handle POST request
        try:
            data_in = str(request.get_json())
            #print(data_in)
            data_raw = data_in.replace("{", "").replace("}", "").replace("'", "").replace(":", "_")
            #print(data_raw)
            data = data_raw.split("_")
            pixels[int(data[0])][int(data[1])] = int(data[2])

            #print('updated')  # yeah that works
            #print(pixels[int(data[0])][int(data[1])])
            return 'POST request received'
        except:
            return 'failed'


if __name__ == '__main__':
    bg_thread = Thread(target=background_task)
    bg_thread.start()
    app.static_folder = 'static'
    app.run(port=8080, host='0.0.0.0', debug=False, use_reloader = True)
