# CONFIGURATION VARIABLES of Project
LABELS = ['hiphop' 'dohori' 'adhunik' 'filmy' 'pop']
PATH_TO_MODEL = 'Model/final/finalModel'
PATH_TO_WEIGHTS = 'Model/final/final_weights'


# important on backend

import logging
logging.getLogger("tensorflow").setLevel(logging.ERROR)

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import sys
import numpy as np
import librosa
import datetime
import traceback
import tensorflow.keras as keras

help_message = '''
        Usage: Classifies Genre from Audio File using CNN

        Syntax:

        $ python classifer.py -input path/to/audio_file
'''

def prepare_input(file_path):    
    num_mfcc = 13
    n_fft = 2048
    hop_length = 512
    SAMPLE_RATE = 22050
    segment_size = 66150
    signal, sr = librosa.load(file_path, sr=SAMPLE_RATE, duration=30)
    start = segment_size * 1
    end = start + segment_size
    mfcc = librosa.feature.mfcc(signal[:segment_size], SAMPLE_RATE, n_mfcc=num_mfcc, n_fft=n_fft, hop_length=hop_length)
    mfcc = mfcc.T

    mfcc = mfcc[..., np.newaxis]
    return mfcc


def predict(model, X, y=""):

    # add a dimension to input data for sample - model.predict() expects a 4d array in this case
    X = X[np.newaxis, ...] # array shape (1, 130, 13, 1)

    # perform prediction
    prediction = model.predict(X)

    # get index with max value
    predicted_index = np.argmax(prediction, axis=1)

    return int(predicted_index)


def find_genre_from_audio(audio_file):
    try:
        print("Start: ", datetime.datetime.now().strftime("%H:%M:%S"))
        print("Audio File: ", audio_file)
        print("Extracting Features .. ")
        # Feature Extraction from audio
        audio_to_predict = prepare_input(audio_file)

        # Load Model
        print("Loading Model .. ")
        model = keras.models.load_model(PATH_TO_MODEL)

        # Load Weights to Model
        print("Loading Weights .. ")
        model.load_weights(PATH_TO_WEIGHTS)
        
        # Make Prediction
        print("Making Prediction .. ")
        genre_index = predict(model, audio_to_predict)

        return {'genre': LABELS[genre_index], 'success': True}
    except:
        traceback.print_exc()
        print('---------------')
        return {'genre': 'Unknown', 'success': False}


def get_flag_value(flag):
    try:
        return sys.argv[sys.argv.index('-' + flag) + 1]
    except:
        print("Error: Value of {} not found".format(flag))


if __name__ == '__main__':
    input_file = get_flag_value('if')
    if not input_file:
        raise Exception("Input Audio File (-if) Required")

    result = find_genre_from_audio(input_file)
    print("->", result, "<-")
    print("END: ", datetime.datetime.now().strftime("%H:%M:%S"))
