from PIL import Image
import numpy as np
import json
import random

sketch_path = "/Users/pondjames007/Desktop/ITP_Classes/Thesis/quickdraw/sketchrnn/"
with open('categories_full.json', 'r') as file:
    sketch_categories = json.load(file)['models']

sketches = []
for _ in range(3):
    sketch = random.choice(sketch_categories)
    stroke = np.load(sketch_path+sketch+'.npz', encoding='latin1')
    sketches.append(random.choice(stroke['train']))

print(sketches)