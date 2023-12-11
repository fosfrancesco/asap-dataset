""" 
This script is useful if you want to perform audio beat tracking.
It takes the asap_annotations.json file and the metadata.csv file and creates the .beats files for the asap dataset.
"""

from pathlib import Path
import json
import pandas as pd
import soundfile as sf
from collections import OrderedDict

BASE_PATH = Path("./")


with open(Path(BASE_PATH,'asap_annotations.json')) as json_file:
    json_data = json.load(json_file)
print("Total performances", len(json_data.keys()))

df = pd.read_csv(Path(BASE_PATH,"metadata.csv"))
# #get a list of performances such as there are not 2 performances of the same piece
# df = df.drop_duplicates(subset=["title","composer"])
# print("Not duplicate", len(df))

# take only the tracks with audio
df = df[df["audio_performance"].notna()]

json_data = {k:json_data[k] for k in df["midi_performance"].values}
print("with audio", len(json_data.keys()))

# remove pieces with multiple time signatures
tsc_pieces = {k:v for k,v in json_data.items() if len(v["perf_time_signatures"])==1 }
print("Only 1 time signature", len(tsc_pieces))

# remove pieces that have bR in the beat annotations
no_br_pieces = {k:v for k,v in tsc_pieces.items() if not any([beat_type == "bR" for time,beat_type in v["performance_beats_type"].items()])}
print("No bR", len(no_br_pieces))

# get the remaining unique time signatures
unique_ts = set()
for k,v in no_br_pieces.items():
    print(v["perf_time_signatures"])
    print(list(v["perf_time_signatures"].values()))
    unique_ts.add(list(v["perf_time_signatures"].values())[0][1])
print("Time signatures numerators", unique_ts)


def anndict_to_beats(anndict, output_path, number_of_beats):
    # write a tsv file with beats.times as first column and beats.positions as second column
    ordered_ann = OrderedDict(sorted(anndict.items(), key = lambda x: float(x[0])))
    with open(output_path, 'w') as f:
        # find how many beats before the first downbeat
        first_downbeat_index = [i for i, x in enumerate(ordered_ann.values()) if x == "db"][0]
        upmeasure = [number_of_beats - i for i in range(first_downbeat_index)][::-1]
        # find and write the beats
        counter = 1
        for i, (time,type) in enumerate(ordered_ann.items()):
            if type == "db":
                counter = 1
                pos = 1
            elif type == "b":
                if i < first_downbeat_index:
                    pos = upmeasure[0]
                    upmeasure.pop(0)
                elif i>= first_downbeat_index:
                    pos = counter
                else:
                    raise ValueError("Something went wrong")
            else:
                raise ValueError("Something went wrong")
            counter += 1
            f.write(str(time) + '\t' + str(pos) + '\n')

# save audio and beat annotations in tsv .beats format
for k,v in no_br_pieces.items():
    audio_performance_path = df[df["midi_performance"]==k]["audio_performance"].values[0]
    path_flattened = audio_performance_path.replace('/','_')[:-4]
    ann_path = str(Path("asap_beat","annotations","beats",f"{path_flattened}.beats"))
    audio_path = str(Path("asap_beat","audio",f"{path_flattened}.flac"))
    # save audio
    audio, sr = sf.read(audio_performance_path)
    sf.write(audio_path, audio, sr)
    # save beat annotations
    anndict_to_beats(v["performance_beats_type"], ann_path, list(v["perf_time_signatures"].values())[0][1])