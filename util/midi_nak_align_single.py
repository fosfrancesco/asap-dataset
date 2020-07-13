import pandas as pd
from pathlib import Path
import subprocess

########## This FILE WORK ONLY IN LINUX (no windows supported)#############

MAESTRO_BPATH = Path("../datasets/maestro-v2.0.0/")  #you need to download the maestro dataset from https://magenta.tensorflow.org/datasets/maestro
BASE_PATH = Path("./")
NAK_PATH = Path("./util/nak_alignment")
NAK2DS_PATH = Path("../../")


all_df = pd.read_csv(Path(BASE_PATH,"ASAP_v1.csv"))
df = all_df[all_df.score_midi == "Schubert/Impromptu_op142/3/midi_cleaned.mid"].copy()


def delete_old_files(row):
    #delete the old alignment files
    Path(BASE_PATH,row["performed_midi_path"][:-4]+"_infer_corresp.txt").unlink()
    Path(BASE_PATH,row["performed_midi_path"][:-4]+"_infer_match.txt").unlink()
    Path(BASE_PATH,row["performed_midi_path"][:-4]+"_infer_spr.txt").unlink()

def generate_nak_align(row):
    subprocess.call([Path(NAK_PATH,"MIDIToMIDIAlign.sh"), Path(BASE_PATH,row["score_midi"][:-4]), Path(row["performed_midi_path"][:-4])])

# def update_corresp_path(row):
#     if pd.isnull(row["maestro_path"]):
#         return row["midi2midi_alignment_path"]
#     else:
#         return row["midi2midi_alignment_path"].replace("_infer_corresp.txt","M_corresp.txt")



print("Processing ..................")
for i, row in df.iterrows():
    print("Aligning",row["performed_midi_path"])
    try:
        generate_nak_align(row)
        # delete_old_files(row)
    except Exception as e:
        print("!!!!!!Failed", e)

# print("Updating the corresp ................")
# df["midi2midi_alignment_path"] =df.apply(update_corresp_path,axis = 1) 

#save the new dataframe
# df.to_pickle("performance_dataframe_v2(bach).pkl")