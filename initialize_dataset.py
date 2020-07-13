"""Given a correspondence.csv file from alignment.py, this script will set up (copy and crop)
the dataset files."""
import argparse
import pandas as pd
import os
import librosa
from shutil import copyfile
import numpy as np
from pathlib import Path   
    
    
def clip_and_copy_audio(in_path, out_path, start=None, end=None, padding=0.5):
    """
    Clip the given wav file (if desired), and copy it to a new location.
    
    Parameters
    ----------
    in_path : string
        Path of the input wav file.
        
    out_path : string
        Output path for the resulting wav file.
        
    start : float
        Starting time (in seconds) of the output file. (This many seconds will be clipped
        from the beginning of the input.) None for no start clipping.
        
    end : float
        Endd time (in seconds) for the output file. (The final sample in the output file
        will be the sample at this time in the input file.) None for no end clipping.
        
    padding : float
        Padding (in seconds) to add to the beginning of the piece if start is greater than
        this amount. That is, instead of shifting the audio at the start time to
        time 0, it is shifted to this time, and the beginning is padded with 0s. However, no
        sound will ever be shifted forward of its original time due to this value (so if
        padding > start, it is instead set to start).
    """
    if np.isnan(start) and np.isnan(end):
        if in_path != out_path:
            copyfile(in_path, out_path)
        return
    
    s = 0.0 if np.isnan(start) else start
    dur = None if np.isnan(end) else end - s
    data, sr = librosa.core.load(in_path, sr=None, mono=False,
                                 offset=s,
                                 duration=dur)
    
    
    # Pad with 0s
    if s > 0:
        samples = int(sr * padding)
        if len(data.shape) == 1:
            # Mono
            zeros = np.zeros(samples)
            data = np.append(zeros, data)
        else:
            # Stereo (or more)
            zeros = np.zeros((data.shape[0], samples))
            data = np.asfortranarray(np.concatenate( (zeros,data),axis=1))
    
    librosa.output.write_wav(out_path, y=data.astype(np.float32), sr=sr, norm=False)



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Initialize the performed_midi dataset by '
                                     'cutting maestro audio files and moving them into their correct locations.',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    parser.add_argument('-m', '--maestro', help='The location of the downloaded maestro data.',
                        default='../maestro-v2.0.0', type=str)
        
    parser.add_argument('--metadata', help='The correspondence.csv metadata file.',
                        default='metadata.csv', type=pd.read_csv)
    
    args = parser.parse_args()
    
    print("Cutting and copying maestro audio performances")
    counter = 0
    for idx, row in args.metadata.iterrows():
        if not row.isna()["maestro_audio_performance"]:
            try:
                maestro_path = str(Path(row["maestro_audio_performance"])).replace('{maestro}', str(args.maestro))
                clip_and_copy_audio(str(maestro_path),
                                    str(Path(row["audio_performance"])),
                                    start=row.start, end=row.end)
            except Exception as e:
                print("Failed for", idx,row["midi_performance"])
                print(e)
            counter+=1
        if counter%20 == 0:
            print("{}/520 completed".format(counter))
