import re
import os
import asyncio
import random
import string
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import aiohttp
import numpy as np
import io
from PIL import Image
from io import BytesIO
import json
from aiohttp import web

# Load the model and class_dict as you did in your code
model = tf.keras.models.load_model('pokemon_lol.h5')
class_dict = {}
with open('predict.txt', 'r', encoding='utf-8') as file:
    for line in file:
        index, class_name = line.strip().split(':')
        class_dict[int(index)] = class_name

async def predict_pokemon(request):
    data = await request.json()
    image_url = data.get('image_url')

    if not image_url:
        return web.Response(status=400, text='Bad Request: Image URL is missing.')

    async with aiohttp.ClientSession() as session:
        async with session.get(image_url) as response:
            if response.status == 200:
                image_bytes = await response.read()

                img = image.load_img(io.BytesIO(image_bytes), target_size=(64, 64))
                img = image.img_to_array(img)
                img = np.expand_dims(img, axis=0)
                img /= 255.0

                prediction = model.predict(img, verbose=0)
                predicted_class_index = np.argmax(prediction)
                pokemon_name = class_dict.get(predicted_class_index, "Unknown")

                # Convert predicted_class_index to a serializable data type (e.g., int)
                predicted_class_index = int(predicted_class_index)

                result = {
                    "predicted_class_index": predicted_class_index,
                    "pokemon_name": pokemon_name
                }
                return web.Response(text=json.dumps(result), content_type='application/json')
            else:
                return web.Response(status=response.status, text='Failed to fetch the image.')

app = web.Application()
app.router.add_post('/predict_pokemon', predict_pokemon)

web.run_app(app, host='0.0.0.0', port=8080)
