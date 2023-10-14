import re
import os
import asyncio
import random
import string
import discord
from discord.ext import commands
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import requests
import typing
import numpy as np
import io
from PIL import Image
from io import BytesIO
import aiohttp
import re
import json
import time
current_time = time.time()

# Convert the current time to a human-readable format
time_ = time.strftime("%H:%M:%S", time.localtime(current_time))

def load_config():
    with open("config.json", "r") as f:
        return json.load(f)

from python_anticaptcha import AnticaptchaClient, ImageToTextTask

def clear_terminal():
    os.system("cls" if os.name == "nt" else "clear")

config = load_config()
channel_id = config.get("channel_id")
pokemon = config.get("pokemon_id")
version = 'v2'

# Create the bot with the intents
client = discord.Client()

model = tf.keras.models.load_model('pokemon_lol.h5')

# Load class names and indices from "predict.txt"
class_dict = {}
with open('predict.txt', 'r', encoding='utf-8') as file:
  for line in file:
    index, class_name = line.strip().split(':')
    class_dict[int(index)] = class_name

# def print_blue(message):
#     print(f"\033[94m[{time_}][CONFIG]{message}\033[0m")

# def print_success(message):
#     print(f"\033[32m[{time_}][SUCCESS]{message}\033[0m")

# def print_failure(message):
#     print(f"\033[31m[{time_}][ERROR]{message}\033[0m")

# def print_in_progress(message):
#     print(f"\033[33m[{time_}][IN_PROGRESS]{message}\033[0m")

# @client.event
# async def on_ready():
#   print_success("V2 - PokeMon")
#   print_success(f'Logged into account: {client.user.name}')


@client.event
async def on_message(message):
  channel = message.channel
  if message.author.id == pokemon:
    if message.embeds:
      for embed in message.embeds:
        if embed.title and 'appeared!' in embed.title:
          # Extract the image URL from the embed
          image_url = embed.image.url
          async with aiohttp.ClientSession() as session:
            async with session.get(image_url) as response:
              if response.status == 200:
                image_bytes = await response.read()

                # Load the image using io.BytesIO
                img = image.load_img(io.BytesIO(image_bytes),
                                     target_size=(64, 64))
                img = image.img_to_array(img)
                img = np.expand_dims(img, axis=0)  # Add a batch dimension
                img /= 255.0  # Rescale to [0, 1] since the model was trained with rescaling

                # Make predictions using the image classification model
                prediction = model.predict(img, verbose=0)

                # Get the predicted class label index
                predicted_class_index = np.argmax(prediction)

                # Get the corresponding class name from class_dict
                pokemon_name = class_dict.get(predicted_class_index, "Unknown")
                # Fetch the Pokemon name from the database based on the hash
                print_in_progress(f"Trying to catch {pokemon_name}")
                await channel.send(f"<@{pokemon}> c {pokemon_name}")
                print_success(f"Successfully Caught {pokemon_name}")

        else:
          return



token = config.get("token")
client.run(token)
