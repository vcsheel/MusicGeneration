import sys,os
import matplotlib.pyplot as plt
import numpy as np
import pickle
import glob
import random
from music21 import converter, instrument, note, chord, stream, tempo
from keras.layers import Input, Dense, Reshape, Dropout, LSTM, Bidirectional
from keras.layers import BatchNormalization, Activation, ZeroPadding2D
from keras.layers.advanced_activations import LeakyReLU
from keras.models import Sequential, Model
from keras.models import load_model
# from keras.layers import Dense
# from keras.layers import Dropout
from keras.callbacks import ModelCheckpoint, History
from keras.optimizers import Adam
from keras.utils import np_utils


def get_notes():
    print("HELLO")
    """ Get all the notes and chords from the midi files """
    notes = []
    with open('./notes_maestro_edit2', 'rb') as filepath:
       notes = pickle.load(filepath)

#     for file in glob.glob("/content/gdrive/My Drive/Classical-Piano-Composer/2017/*.midi"):
#         print("IN")
#         midi = converter.parse(file)

#         print("Parsing %s" % file)

#         notes_to_parse = None

#         try: # file has instrument parts
#             s2 = instrument.partitionByInstrument(midi)
#             notes_to_parse = s2.parts[0].recurse() 
#         except: # file has notes in a flat structure
#             notes_to_parse = midi.flat.notes
            
#         for element in notes_to_parse:
#             if isinstance(element, note.Note):
#                 notes.append(str(element.pitch))
#             elif isinstance(element, chord.Chord):
#                 notes.append('.'.join(str(n) for n in element.normalOrder))
#     with open('/content/gdrive/My Drive/Classical-Piano-Composer/data/notes_maestro_try', 'wb') as filepath:
#         pickle.dump(notes, filepath)       

    return notes

def prepare_sequences(notes, n_vocab):
    """ Prepare the sequences used by the Neural Network """
    # map between notes and integers and back
    pitchnames = sorted(set(item for item in notes))
    note_to_int = dict((note, number) for number, note in enumerate(pitchnames))

    sequence_length = 100
    network_input = []
    output = []
    for i in range(0, len(notes) - sequence_length, 1):
        sequence_in = notes[i:i + sequence_length]
        sequence_out = notes[i + sequence_length]
        network_input.append([note_to_int[char] for char in sequence_in])
        output.append(note_to_int[sequence_out])

    n_patterns = len(network_input)

    # reshape the input into a format compatible with LSTM layers
    normalized_input = np.reshape(network_input, (n_patterns, sequence_length, 1))
    # normalize input
    normalized_input = normalized_input / float(n_vocab)
#     print("Network input : ",len(network_input))
#     print("Normalized : ",normalized_input.shape)

    return (network_input, normalized_input)



def create_network(network_input, n_vocab):
    """ create the structure of the neural network """
    model = Sequential()
    model.add(LSTM(512,input_shape=(network_input.shape[1], network_input.shape[2]),return_sequences=True))
    model.add(Dropout(0.3))
    model.add(Bidirectional(LSTM(512, return_sequences=True)))
    model.add(Dropout(0.3))
    model.add(Bidirectional(LSTM(512)))
    model.add(Dense(256))
    model.add(Dropout(0.3))
    model.add(Dense(n_vocab))
    model.add(Activation('softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam')
    model.load_weights("./weights-maestro2-50-0.8343-.hdf5")
    
    return model

def generate_notes(model, notes, network_input, n_vocab,start,seq_length):
    """ Generate notes from the neural network based on a sequence of notes """
    # pick a random sequence from the input as a starting point for the prediction
#     print(type(network_input))
#     print(network_input)
    pitchnames = sorted(set(item for item in notes))
    
#     start = np.random.randint(0, len(network_input)-1)

    int_to_note = dict((number, note) for number, note in enumerate(pitchnames))

    pattern = network_input[start]
    prediction_output = []
    pattern2 = [int_to_note[i] for i in pattern]

    indices = [x for x in range(n_vocab)]

    # generate 500 notes
    for note_index in range(seq_length):
        prediction_input = np.reshape(pattern, (1, len(pattern), 1))
        prediction_input = prediction_input / float(n_vocab)

        prediction = model.predict(prediction_input, verbose=0)
#         prediction_probs = prediction.flatten()
#         index = np.random.choice(indices,size=1,p = prediction_probs)

        index = np.argmax(prediction)
        result = int_to_note[index]
        prediction_output.append(result)
        
#         pattern = np.append(pattern,index)
        pattern.append(index)
        pattern = pattern[1:len(pattern)]
   
    return prediction_output


def create_midi(prediction_output, filename,bpm):
    """ convert the output from the prediction to notes and create a midi file
        from the notes """
    offset = 0
    output_notes = []

    # create note and chord objects based on the values generated by the model
    for pattern in prediction_output:
        # pattern is a chord
        if ('.' in pattern) or pattern.isdigit():
            notes_in_chord = pattern.split('.')
            notes = []
            for current_note in notes_in_chord:
                new_note = note.Note(int(current_note))
                new_note.storedInstrument = instrument.Piano()
                notes.append(new_note)
            new_chord = chord.Chord(notes)
            new_chord.offset = offset
            output_notes.append(new_chord)
        # pattern is a note
        else:
            new_note = note.Note(pattern)
            new_note.offset = offset
            new_note.storedInstrument = instrument.Piano()
            output_notes.append(new_note)
        # increase offset each iteration so that notes do not stack
        offset += 0.5
    
    midi_stream = stream.Stream(output_notes)
    t = tempo.MetronomeMark(number = bpm)
    midi_stream.insert(0,t)

#     midi_stream = stream.Stream(output_notes)
    midi_stream.write('midi', fp='./output.mid')

def generate(start,seq_length,bpm):
  notes = get_notes()

  # Get the number of pitch names
  n_vocab = len(set(notes))

  # Convert notes into numerical input
  network_input, network_output = prepare_sequences(notes, n_vocab)
  model = create_network(network_output, n_vocab)

  prediction_output = generate_notes(model, notes, network_input, len(set(notes)), start, seq_length)
  create_midi(prediction_output, './output',bpm)
  print("DONE")


def midi_generate():
    pass

if __name__ == '__main__':
  
    if int(sys.argv[1])==2:
        midi_generate()
    else:
        s = int(sys.argv[2])
        sample_length = int(sys.argv[3]) 
        bpm = int(sys.argv[4])
        counter = int(sys.argv[5])

        print(s,sample_length,bpm)

        if s!=100:
            start = random.randint(0,570)*s + random.randint(0,570)
        else:
            start = random.randint(0,570)*s + random.randint(0,76)
        # We need to write what number range means how many mins or seconds

        generate(start,sample_length,bpm)  

    path1 = "../client/src/assets/Music/genMusic"+str(counter)+".wav"
    cmd1 = "rm -rf "+path1

    cmd2 = "timidity output.mid -Ow -o "+path1
    print(cmd2)
    #os.system(cmd1)
    os.system(cmd2)
    os.system('find . -name "*.mid" -type f -delete')
    #os.system("ln -s genMusic.wav ../client/src/assets/genMusic.wav")