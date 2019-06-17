from flask import Flask, render_template, make_response, session, Markup
from flask import request, redirect, url_for, jsonify
import json
import os
import io
import requests
import random
from PIL import Image
import base64
import spacy
import numpy as np
from draw_strokes import draw_strokes

# init server
app = Flask(__name__)
app.secret_key = "s3cr3t"
app.debug = True
app._static_folder = os.path.abspath('static/')

imtxt_url = 'http://localhost:8003/query'
attngan_url = 'http://localhost:8004/query'

main_imgs64 = []
descriptions = []
sketches = []
obj_drawn = []

def choose_sourceimg():
    # load source image
    image_path = "/Users/pondjames007/Desktop/ITP_Classes/Thesis/flasktest/source_img/"
    # image_names = []
    image_names = [file for file in os.listdir(image_path) if len(file.split('.')) > 1 and file.split('.')[1] == "jpg"]
    print(image_names)
    image_chosen = random.choice(image_names)
    source_image = Image.open(image_path+image_chosen)

    output_buffer = io.BytesIO()
    source_image.save(output_buffer, format='JPEG')
    byte_data = output_buffer.getvalue()
    source_image64 = str(base64.b64encode(byte_data))
    source_image64 = "data:image/jpg;base64," + source_image64[2:-1]

    return source_image64

def choose_sketches(description, nlp):
    print('\nGetting nouns in the sentence...\n')
    with open('categories_full.json', 'r') as file:
        sketch_categories = json.load(file)['models']
    
    sentence_nlp = nlp(description)
    detect_objs = [word for word in sentence_nlp if word.pos_ is 'NOUN']
    print('Nouns in the sentence: ')
    print(detect_objs)
    sketch_nlp = [nlp(word.replace('_', ' ')) for word in sketch_categories]
    # print(sketch_nlp)
    
    obj_to_draw = []
    for obj in detect_objs:
        similar = [obj.similarity(vec) for vec in sketch_nlp]
        obj_to_draw.append(sketch_nlp[np.argmax(similar)].text)

    sentence = description
    for old, new in zip(detect_objs, obj_to_draw):
        sentence = sentence.replace(old.text, new)

    return obj_to_draw, sentence

def draw_sketch(objs):
    sketch_path = "/Users/pondjames007/Desktop/ITP_Classes/Thesis/quickdraw/sketchrnn/"
    sketch_strokes = []
    for obj in objs:
        data = np.load(sketch_path+obj.replace(' ', '_')+'.npz', encoding='latin1')
        sketch_strokes.append(random.choice(data['train']))

    svg_string = draw_strokes(sketch_strokes)

    return svg_string

# Communicate with client
@app.route('/', methods=['GET'])
def index():
    main_imgs64.clear()
    descriptions.clear()
    sketches.clear()
    obj_drawn.clear()
    return render_template('index.html')
    


@app.route('/', methods=['POST'])
def getData():    
    if request.form.get('loadnlp'):
        global nlp 
        nlp = spacy.load("en_core_web_lg")
        print('nlp loaded')
        return 'nlp loaded'

    if request.form.get('description'):
        print('Description Received: ')
        print(request.form['description'])
        obj_to_draw, new_sentence = choose_sketches(request.form['description'], nlp)
        print('\nObjects to draw: ')
        print(obj_to_draw)
        
        print('\nDrawing the sketch...')
        # print("Drawing...")
        svg_string = draw_sketch(obj_to_draw)
        print('Finish drawing\n')
        print("Connect to Runway AttnGAN\n")
        print("New sentence: ")
        print(new_sentence)
        print("\nSending data to AttnGAN")
        print("Processing...")
        new_image = requests.post(url= attngan_url, json={"caption": new_sentence})
        # print(new_image)
        print("Received New Image")
        main_imgs64.append(new_image.json()['result'])
        sketches.append(svg_string)
        descriptions.append(request.form['description'])
        obj_drawn.append(", ".join(obj_to_draw)) # join to string
        print('Sending new image to client')
        return new_image.json()['result']
    
    if request.form.get('story'):
        print('Sending full story to client')
        story = jsonify({'images': main_imgs64, 'sketches': sketches, 'descriptions': descriptions, 'obj_drawn': obj_drawn})
        return story

    source_iamge = choose_sourceimg()
    main_imgs64.append(source_iamge)
    return source_iamge


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)