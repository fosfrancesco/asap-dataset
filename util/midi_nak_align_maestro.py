import pandas as pd
from pathlib import Path
import subprocess

########## This FILE WORK ONLY IN LINUX (no windows supported)#############

MAESTRO_BPATH = Path("../datasets/maestro-v2.0.0/")  #you need to download the maestro dataset from https://magenta.tensorflow.org/datasets/maestro
VIRTUOSO_BPATH = Path("./")
NAK_PATH = Path("./util/nak_alignment")
NAK2DS_PATH = Path("../../")

all_df = pd.read_csv(Path(VIRTUOSO_BPATH,'correspondence-base-with_vnet.csv'))
matched_full = all_df.loc[~all_df.maestro_title.isna() & ~all_df.vnet_title.isna() & all_df.n.isna()]
align_perf = matched_full[matched_full.vnet_composer != "Bach"]


def delete_old_files(row):
    #delete the old alignment files
    Path(VIRTUOSO_BPATH,row["vnet_performed_midi"][:-4]+"_infer_corresp.txt").unlink()
    Path(VIRTUOSO_BPATH,row["vnet_performed_midi"][:-4]+"_infer_match.txt").unlink()
    Path(VIRTUOSO_BPATH,row["vnet_performed_midi"][:-4]+"_infer_spr.txt").unlink()

def generate_nak_align(row):
    subprocess.call([Path(NAK_PATH,"MIDIToMIDIAlign.sh"), Path(VIRTUOSO_BPATH,row["score_midi"][:-4]), Path(row["vnet_performed_midi"][:-4]+"M")])

def update_corresp_path(row):
    if pd.isnull(row["maestro_path"]):
        return row["midi2midi_alignment_path"]
    else:
        return row["midi2midi_alignment_path"].replace("_infer_corresp.txt","M_corresp.txt")



print("Creating ..................")
align_perf.apply(generate_nak_align,axis = 1)
print("Deleting old files ......................")
align_perf.apply(delete_old_files,axis = 1)
# print("Updating the corresp ................")
# df["midi2midi_alignment_path"] =df.apply(update_corresp_path,axis = 1) 

#save the new dataframe
# df.to_pickle("performance_dataframe_v2(bach).pkl")