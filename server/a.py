import sys 
import os
import glob
import pickle
import numpy as np
import random
from music21 import instrument, note, stream, chord,tempo,converter
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.layers import Activation



def generate(start,sample_length,bpm):
    """ Generate a piano midi file """
    #load the notes used to train the model
    with open('./notes', 'rb') as filepath:
        notes = pickle.load(filepath)

    # Get all pitch names
    pitchnames = sorted(set(item for item in notes))
    # Get all pitch names
    n_vocab = len(set(notes))-1

    network_input, normalized_input = prepare_sequences(notes, pitchnames, n_vocab)
    model = create_network(normalized_input, n_vocab)
    prediction_output = generate_notes(model, network_input, pitchnames, n_vocab,start,sample_length,bpm)
    create_midi(prediction_output)

def prepare_sequences(notes, pitchnames, n_vocab):
    """ Prepare the sequences used by the Neural Network """
    # map between notes and integers and back
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

    return (network_input, normalized_input)


def create_network(network_input, n_vocab):
    """ create the structure of the neural network """
    model = Sequential()
    model.add(LSTM(
        512,
        input_shape=(network_input.shape[1], network_input.shape[2]),
        return_sequences=True
    ))
    model.add(Dropout(0.3))
    model.add(LSTM(512, return_sequences=True))
    model.add(Dropout(0.3))
    model.add(LSTM(512))
    model.add(Dense(256))
    model.add(Dropout(0.3))
    model.add(Dense(n_vocab))
    model.add(Activation('softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='rmsprop')

    # Load the weights to each node
    model.load_weights('./weights-improvement-78-0.8215-bigger.hdf5')

    return model



def generate_notes(model, network_input, pitchnames, n_vocab,start,sample_length,bpm):
    """ Generate notes from the neural network based on a sequence of notes """
    # pick a random sequence from the input as a starting point for the prediction
#     start = np.random.randint(0, len(network_input)-1)

    int_to_note = dict((number, note) for number, note in enumerate(pitchnames))

    pattern = network_input[start]    #<--- taking sample from training
    print(pattern)
    pattern2 = [int_to_note[i] for i in pattern]
    prediction_output = []
    indices = [x for x in range(358)]
  
    # generate 500 notes
    for note_index in range(sample_length):
        prediction_input = np.reshape(pattern, (1, len(pattern), 1))
        prediction_input = prediction_input / float(n_vocab)

        prediction = model.predict(prediction_input, verbose=0)
#         print("AAAA : ",prediction.shape)
        prediction_probs = prediction.flatten()
        # index = np.random.choice(indices,size=1,p = prediction_probs)

        index = np.argmax(prediction)
        # result = int_to_note[index[0]]
        result = int_to_note[index]
#         print(index," :  ",result)
        prediction_output.append(result)

        pattern.append(index)
        pattern = pattern[1:len(pattern)]
#     print(len(prediction_output))
    print(prediction_output)
    return prediction_output

def midi_generate():
    notes = []

    for file in glob.glob("./*.mid"):
        midi = converter.parse(file)

        print("Parsing %s" % file)

        notes_to_parse = None

        try: # file has instrument parts
            s2 = instrument.partitionByInstrument(midi)
            notes_to_parse = s2.parts[0].recurse() 
        except: # file has notes in a flat structure
            notes_to_parse = midi.flat.notes

        for element in notes_to_parse:
            if isinstance(element, note.Note):
                notes.append(str(element.pitch))
            elif isinstance(element, chord.Chord):
                notes.append('.'.join(str(n) for n in element.normalOrder))
    start = notes[:100]
    with open('./notes', 'rb') as filepath:
        notes = pickle.load(filepath)

    # Get all pitch names
    pitchnames = sorted(set(item for item in notes))
    # Get all pitch names
    n_vocab = len(set(notes))-1
    network_input, normalized_input = prepare_sequences(notes, pitchnames, n_vocab)
    print(normalized_input.shape)
    model = create_network(normalized_input, n_vocab)
    int_to_note = dict((number, note) for number, note in enumerate(pitchnames))
    note_to_int = dict((note,number) for number,note in int_to_note.items())
    pattern = [note_to_int[i] for i in start]
    print(len(pattern))
    # print(network_input[0])
    prediction_output = []
    indices = [x for x in range(358)]
  
    # generate 500 notes
    for note_index in range(200):
        prediction_input = np.reshape(pattern, (1, len(pattern), 1))
        prediction_input = prediction_input / float(n_vocab)

        prediction = model.predict(prediction_input, verbose=0)
#         print("AAAA : ",prediction.shape)
        prediction_probs = prediction.flatten()
        # index = np.random.choice(indices,size=1,p = prediction_probs)

        index = np.argmax(prediction)
        # result = int_to_note[index[0]]
        result = int_to_note[index]
#         print(index," :  ",result)
        prediction_output.append(result)

        pattern.append(index)
        pattern = pattern[1:len(pattern)]
#     print(len(prediction_output))
    print(prediction_output)
    create_midi(prediction_output)


def create_midi(prediction_output,bpm = 120):
    """ convert the output from the prediction to notes and create a midi file
        from the notes """
    offset = 0
    output_notes = []
#     print(prediction_output)
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

    midi_stream.write('midi', fp='./output.mid')


if __name__ == "__main__":
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
