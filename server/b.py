from music21 import stream, instrument
from music21.note import Note

n = Note("A2", type='quarter')

drumPart = stream.Part()
drumPart.insert(0, instrument.Woodblock())

drumMeasure = stream.Measure()
drumMeasure.append(n)
drumPart.append(drumMeasure)

# This line actually generate the midi on my mac but there is no relevant software to read it and the opening fail
drumPart.show('midi')
