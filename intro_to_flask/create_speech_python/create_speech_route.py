import os
import openai
from openai import OpenAI
import re #regular expressions module
from markupsafe import escape #protects projects against injection attacks
from intro_to_flask import app
import sys 
sys.dont_write_bytecode = True
from flask import render_template, request, Flask, Blueprint
from .create_speech_form import CreatespeechForm #removed draw and added createspeech
from pathlib import Path #added path for tts?

createSpeech_blueprint = Blueprint('create_speech', __name__)

@createSpeech_blueprint.route('/create_speech',methods=['GET', 'POST'])
@app.route('/create_speech',methods=['GET', 'POST'])
def create_speech():
  form = CreatespeechForm(request.form) #replace with createspeech class
  
  if request.method == 'POST':
      if form.validate() == False:
        return render_template('create_speech.html', form=form)
      else:
        # The following response code adapted from example on: 
        # https://platform.openai.com/docs/guides/text-to-speech
        client = OpenAI()

        speech_file_path = Path(__file__).parent /  "speech.mp3" #code from tts api
        response = client.audio.speech.create( #changed to tts style
          model="tts-1", #changed model 
          voice = "alloy", #added voice (part of tts api)
          input=form.prompt.data #og prompt=form.prompt.data
          #removed quality, size, and n
        )

        display_sound_bar = response.stream_to_file(speech_file_path)
        
        #display_image_url = response.data[0].url 
        return render_template('create_speech.html', create_speech_prompt=form.prompt.data,create_speech_response=display_sound_bar,success=True)
        #replaced with create_speech.html
  elif request.method == 'GET':
      return render_template('create_speech.html', form=form)
        #replaced with create_speech.html