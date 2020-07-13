import pandas as pd
from pathlib import Path
import subprocess

########## This FILE WORK ONLY IN LINUX (no windows supported)#############

MAESTRO_BPATH = Path("../datasets/maestro-v2.0.0/")  #you need to download the maestro dataset from https://magenta.tensorflow.org/datasets/maestro
VIRTUOSO_BPATH = Path("./")
NAK_PATH = Path("./util/nak_alignment")
NAK2DS_PATH = Path("../../")

df = pd.read_pickle("quant_dataframe.pkl")

print("Generating score2midi match file for:",df.shape[0],"files")

# def generate_nak_align(row):
#     print("generating for file", row["opus"])
#     subprocess.call([Path(NAK_PATH,"MusicXMLToMIDIAlign.sh"), Path(VIRTUOSO_BPATH,row["opus"],"musicxml_cleaned"), Path(VIRTUOSO_BPATH,row["opus"],"midi_cleaned")])
#     print("-------------------------------------------------")
#   
# print("Creating ..................")
# df.apply(generate_nak_align,axis = 1)
# print("Done")

subprocess.call([Path(NAK_PATH,"MusicXMLToMIDIAlign.sh"), Path(VIRTUOSO_BPATH,"Bach/Fugue/bwv_848/musicxml_cleaned"), Path(VIRTUOSO_BPATH,"Bach/Fugue/bwv_848/midi_cleaned")])