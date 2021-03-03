# CONFIGURATION VARIABLES of Project
LABELS = ['Pop', 'Filmy', 'Adhunik', 'Dohori']
PATH_TO_MODEL = 'Model/deepModel'
PATH_TO_WEIGHTS = 'Model/weights'


# important on backend
import sys
import numpy as np
import librosa
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
    signal, sr = librosa.load(file_path, sr=SAMPLE_RATE)
    start = segment_size * 1
    end = start + segment_size
    mfcc = librosa.feature.mfcc(signal[start:end], SAMPLE_RATE, n_mfcc=num_mfcc, n_fft=n_fft, hop_length=hop_length)
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

    return LABELS[genre_index]


def get_flag_value(flag):
    try:
        return sys.argv[sys.argv.index('-' + flag) + 1]
    except:
        print("Error: Value of {} not found".format(flag))


if __name__ == '__main__':
	input_file = get_flag_value('input')
	if not input_file:
		raise Exception("Input Audio File Required")

	find_genre_from_audio(input_file)
