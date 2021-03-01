import pandas as pd
import music21 as m21
import pretty_midi as pm
import numpy as np

from pathlib import Path

def ts2n_of_beats(ts):
    """Get the number of beats in a given time signature according to music theory

    Arguments:
        ts {string} -- the time signature [numerator]/[denominator]

    Raises:
        TypeError: if the ts string is not in the correct format

    Returns:
        int -- the number of beats
    """
    num = int(ts.split("/")[0])
    if num == 1:
        return 1
    elif num == 2 or num == 6: #duple meter
        return 2
    elif num == 3 or num == 9: #triple meter
        return 3
    elif num == 4 or num == 12: #quadruple meter
        return 4
    elif num == 5:
        return 5
    elif num == 24: #my choice
        return 8
    else: #complex meter
        raise TypeError("The meter is not supported")


def check_annotation_text(annotations_path, allow_W_flag = False):
    """Check the type of annotation for a text file (name, key signature, time signature) and print warnings if there are problems

    Arguments:
        annotations_path {string} -- the path of the annotation text file
        allow_W_flag {boolean} -- ignore the W flag used for annotation cleaning in name
    """
    ann_df = pd.read_csv(annotations_path,header=None, names=["time","time2","type"],sep='\t')
    allowed_names = ["db","b","bR"]

    warnings = []
    for i, r in ann_df.iterrows():
        #check the ann type (db,b or bR)
        if allow_W_flag:
            name = r["type"].split(",")[0] if r["type"].split(",")[0][-1]!= "W" else r["type"].split(",")[0][:-1]
        else:
            name = r["type"].split(",")[0]
        if not name in allowed_names:
            warnings.append("Wrong name " + str(r["type"].split(",")[0] ,"at", r["time"]))
        #check the time signature
        if len(r["type"].split(","))==2 or (len(r["type"].split(","))==3 and r["type"].split(",")[1]!=""):
            try:
                ts2n_of_beats(r["type"].split(",")[1])
            except:
                warnings.append("Wrong ts" + str(r["type"].split(",")[1]))
        #check the key signature
        if len(r["type"].split(","))==3:
            if not int(r["type"].split(",")[2]) in list(range(-7,8)):
                warnings.append("Wrong ks" + str(r["type"].split(",")[2]))

    if len(warnings) > 0:
        print("Annotation text problems in",annotations_path )
        print(warnings)


def check_b_db_ratio(annotations_path):
    """Check if the ratio beats, downbeats is correct according to the time signature and print warnings if there are problems
    The ration can be different of what expected if at least one "bR" is in the measure

    Arguments:
        annotations_path {string} -- the path of the annotation text file
    """
    warnings = []

    ann_df = pd.read_csv(annotations_path,header=None, names=["time","time2","type"],sep='\t')
    ann_df = ann_df.sort_values(by=['time'])
    #clean the W flag (used for annotations cleaning)
    merged_annotations = [(row["time"],row["type"]) if row["type"][-1]!="W" else (row["time"],row["type"][:-1])  for i,row in ann_df.iterrows()]

    try:
        #check if the correct number of beat every downbeat
        counter = 1
        pickup = True
        rubato = False
        for ann in merged_annotations:  
            #set the eventual rubato flag
            if ann[1].split(",")[0][-1]=="R":
                rubato = True
            #start checking the beats and downbeats
            if ann[1].split(",")[0] == "db":
                if pickup: #first db of the non pickup, don't check
                    pass
                elif rubato: #first db after rubato, don't check
                    pass
                else: #we check the counter
                    if counter != number_of_beats:  
                        warnings.append("Checking ratio for opus " + str(annotations_path))
                        warnings.append("Wrong number of beats: (" + str(counter) + ") in ann" + str(ann[0]//60) + "m" + str(ann[0]%60) + ". Expecting"+ str(number_of_beats))
                pickup = False
                rubato = False
                counter = 1
            elif ann[1][0] == "b": #count "b" and "bR"
                counter += 1
                if (not pickup) and (not rubato):
                    if counter> number_of_beats:
                        warnings.append("Checking ratio for opus" + str(annotations_path))
                        warnings.append("Wrong number of beats: (" + str(counter) +  ") in ann" + str(ann[0]//60) +"m"+ str(ann[0]%60) + ". Expecting"+ str(number_of_beats))
                        
            else:
                counter = 1
                warnings.append("Wrong annotation kind", ann[1], "in time",ann[0])
            #set the time signature and number of beats
            if len(ann[1].split(","))>1 and ann[1].split(",")[1]!= "":
                number_of_beats = ts2n_of_beats(ann[1].split(",")[1])
        
        if len(warnings) > 0:
            print("Beats downbeats ratio problems in",annotations_path )
            print(warnings)
    except:
        print("Exception for", annotations_path)


def check_inverted_annotations(annotations_path):
    "Check if annotations are saved in chronological order."
    ann_df = pd.read_csv(annotations_path,header=None, names=["time","time2","type"],sep='\t')
    for i,row in ann_df.iterrows():
        if row["time"]!=row["time2"]:
            print("Time different from time2 in",annotations_path )
    time_list = ann_df["time"]
    for i,t in enumerate(time_list):
        if i!=0:
            if t<time_list[i-1]:
                print("Inverted annotations for",annotations_path ,"at time", t//60,"m",t%60 )


exception_dict = {
    "Beethoven/Piano_Sonatas/29-2/xml_score.musicxml": {112:[113]},
    "Beethoven/Piano_Sonatas/29-4/xml_score.musicxml": {0:[1],2:[3,4],12:[13,14,15]},
    "Beethoven/Piano_Sonatas/30-1/xml_score.musicxml" : {15:[16],66:[67]},
    "Beethoven/Piano_Sonatas/31-3_4/xml_score.musicxml": {4:[5,6],7:[8,9]},
    "Haydn/Keyboard_Sonatas/49-1/xml_score.musicxml" : {131:[132]},
    "Liszt/Gran_Etudes_de_Paganini/2_La_campanella/xml_score.musicxml" : {97: [98], 99:[100]},
    "Liszt/Mephisto_Waltz/xml_score.musicxml" : {857: [858],198:[199],808: [809,910]},
    "Liszt/Transcendental_Etudes/4/xml_score.musicxml": {23: [24,25],56:[57,58,59]},
    "Liszt/Transcendental_Etudes/9/xml_score.musicxml": {45:[46],75:[76]},
    "Mozart/Fantasie_475/xml_score.musicxml": {84: [85]},
    "Schumann/Kreisleriana/2/xml_score.musicxml": {38:[39],57:[58],96: [97]}
}

repetition_not_working = {
    "Beethoven/Piano_Sonatas/11-3/xml_score.musicxml" : list(range(0,9))*2+list(range(9,32))*2+list(range(32,41))*2+list(range(41,50))+list(range(41,49))+[50]+list(range(0,32)),
    "Beethoven/Piano_Sonatas/28-2/xml_score.musicxml" : list(range(0,9)) + list(range(1,8)) + list(range(9,56)) + list(range(13,55)) + [56,57] + list(range(58,68))*2 + list(range(68,98)) + list(range(1,8))+ list(range(9,55)) + [56],
    "Beethoven/Piano_Sonatas/7-3/xml_score.musicxml" : list(range(0,17))*2 + list(range(17,56))*2 + list(range(56,89)) + list(range(0,56))
}


def same_number_of_measures_with_repetitions(score_xml_path, quantized_annotations_path, base_path="./"):
    """Check if the number of db in the annotations is the same of the (corrected) number of measures in the xml score.
    Many correction has to be done to the number of measure in the scores.
    In some extreme cases, the correction are hardcoded in exception_dict (connected measures) and repetition_not_working (dc al fine music21 exception).

    Arguments:
        score_xml_path {string} -- path of the xml score
        quantized_annotations_path {string} -- path of the midi score annotations

    Returns:
        [list] -- the corresponding measure number for each db in annotation
    """
    complete_score_path = str(Path(base_path,score_xml_path))
    #compute the measure map in the score
    score = m21.converter.parse(complete_score_path)
    #consider both hands because of some durations problems some measures has duration 0
    score_measures_r = score.parts[0].recurse().getElementsByClass(m21.stream.Measure)
    score_measures_l = score.parts[1].recurse().getElementsByClass(m21.stream.Measure)
    if len(score.parts[0].recurse().getElementsByClass(m21.repeat.RepeatMark)) == 0:
        #no repetitions, we are going linearly
        m_map = list(range(len(score_measures_r)))
    elif score_xml_path in repetition_not_working.keys() :
        #in case of dc al fine, music21 does not work. We did it manually
        m_map = repetition_not_working[score_xml_path]
    else:
        try:
            e = m21.repeat.Expander(streamObj= score.parts[0])
            m_map = e.measureMap()
        except:
            print("Processing", score_xml_path )
            print("Expansion Exception")
            return np.nan
        
    #consider pickup measure in the score
    if score_measures_r[0].paddingLeft > 0 or score_measures_l[0].paddingLeft > 0 :
        m_map = m_map[1:]
    else: # or if there is a pause as first event
        some_notes_on_first_db = False
        for part in score.parts:
            measure = part.recurse().getElementsByClass(m21.stream.Measure)[0]
            notes_on_db = [n for n in measure.recurse().notes if n.beat == 1]
            if len(notes_on_db)!= 0:
                some_notes_on_first_db = True
                break
        if not some_notes_on_first_db:
            m_map = m_map[1:]
        
    score_measures_n = len(m_map)
    
    #compute number of measures in the midi score (e.g. in the midi score annotations)
    quant_ann_df = pd.read_csv(quantized_annotations_path,header=None, names=["time","time2","type"],sep='\t')
    len_ann= len([db_tp.split(",")[0] for db_tp in quant_ann_df["type"].tolist() if db_tp.split(",")[0] == "db" ])
      
    if len_ann== score_measures_n: # if it's already aligned, finish here to spare computation time
        return list(m_map)
    else: # consider the splitted measures
        new_map = []
        i =0
        while i < len(m_map):
            # first check if the measure is an exception
            if (not exception_dict.get(score_xml_path) is None) and (m_map[i] in exception_dict[score_xml_path].keys()):
                connected_to = exception_dict[score_xml_path][m_map[i]]
                if len(connected_to) == 1:
                    new_map.append(str(m_map[i])+"-"+str(connected_to[0]))
                    i+=2
                elif len(connected_to) == 2:
                    new_map.append(str(m_map[i])+"-"+str(connected_to[0])+"-"+str(connected_to[1]))
                    i+=3
                elif len(connected_to) == 3:
                    new_map.append(str(m_map[i])+"-"+str(connected_to[0])+"-"+str(connected_to[1])+"-"+str(connected_to[2]))
                    i+=4
                else:
                    print("connected too with too many elements")
            else:
                measure_r = score_measures_r[m_map[i]]
                measure_l = score_measures_l[m_map[i]]
                m_dur = max([measure_r.duration.quarterLength,measure_l.duration.quarterLength]) #actual lenght
                m_ts_dur = max([measure_r.barDuration.quarterLength,measure_l.barDuration.quarterLength]) #lenght from the ts
                if (m_ts_dur == m_dur): 
                    new_map.append(m_map[i])
                    i+=1
                elif (m_ts_dur > m_dur) and i!= len(m_map)-1:
                    next_measure_r = score_measures_r[m_map[i+1]]
                    next_measure_l = score_measures_l[m_map[i+1]]
                    next_m_dur = max([next_measure_r.duration.quarterLength,next_measure_l.duration.quarterLength])
                    next_m_ts_dur= max([next_measure_r.barDuration.quarterLength,next_measure_l.barDuration.quarterLength])
    #                 if (m_dur + next_m_dur == m_ts_dur) and (next_m_ts_dur == m_ts_dur) : #two splitted measures
                    if (m_dur + next_m_dur == m_ts_dur) and (next_m_dur < next_m_ts_dur ) : #two splitted measures, good also if the tempo change if the duration is correct
                        new_map.append(str(m_map[i])+"-"+str(m_map[i+1]))
                        i+=2
                    else:
                        new_map.append(m_map[i])
                        i+=1
                else:
                    new_map.append(m_map[i])
                    i+=1
    
    #consider empty measures at the end of the score or measures with tied chords
    end_index = 0
    found_note = False
    while not found_note:    
        for part in score.parts:
            notes = list(part.recurse().getElementsByClass(m21.stream.Measure)[new_map[-end_index-1]].recurse().notes)
            if len(notes)!= 0:
                for n in notes:
                    if n.isChord:
                        for note in n.notes:
                            if (note.tie is None or note.tie.type == 'start'):
                                found_note = True
                                break
                        if found_note:
                            break
                    else :  #it's a note
                        if (n.tie is None or n.tie.type == 'start'):
                            found_note = True
                            break
        if not found_note:        
            end_index += 1
    if end_index > 0:
        new_map = new_map[:-end_index]
        
    if len_ann== len(new_map):
#         print("Equal")
        return(list(new_map))
    else:
        print("Different",score_xml_path )
        print("Corrected number of measures:",len(new_map),". Number of db in annotations:",len_ann)
        return np.nan

def check_late_early_annot(midi_path, annotations_path):
    """Check if the first annotation time is not earlier than the first note and the last annotation time is not later than last note. Print a warning otherwise

    Arguments:
        midi_path {string} -- path of midi file
        annotationsa_path {string} -- path of the annotations corresponding to the same midi file
    """
    #load annotation file
    ann_df = pd.read_csv(annotations_path,header=None, names=["time","time2","type"],sep='\t')
    first_ann = sorted(ann_df["time"].tolist())[0]
    last_ann = sorted(ann_df["time"].tolist())[-1]

    #load midi file
    midi = pm.PrettyMIDI(midi_path)
    #extract the first note position
    note_ons = midi.get_onsets()
    first_ons = note_ons[0]
    last_ons = note_ons[-1]

    warnings =[]
    #check if the the first annotation is not before the first onset
    if first_ann < first_ons - 0.035: #35 ms accepted window
        warnings.append("Wrong first beat at time "+ str(first_ann) )
        
    #check if the the last annotation is not after the last onset
    if last_ann > last_ons + 0.035: #35 ms accepted window
        warnings.append("Wrong last beat at time "+ str(last_ann) )

    if len(warnings) > 0:
        print("Early late annotations in",annotations_path )
        print(warnings)


def get_beats_from_txt(ann_path):
    """Get the beats time from the text annotations

    Arguments:
        ann_path {string} -- the path of the text annotations

    Returns:
        [list] -- a list of beat onsets
    """
    ann_df = pd.read_csv(Path(ann_path),header=None, names=["time","time2","type"],sep='\t')
    return ann_df["time"].tolist()

def get_downbeats_from_txt(ann_path):
    """Get the downbeats time from the text annotations

    Arguments:
        ann_path {string} -- the path of the text annotations

    Returns:
        [list] -- a list of downbeat onsets
    """
    ann_df = pd.read_csv(Path(ann_path),header=None, names=["time","time2","type"],sep='\t')
    downbeats = [a["time"] for i,a in ann_df.iterrows() if a["type"].split(",")[0] == "db"]
    return downbeats

def get_beats_db_dict_from_txt(ann_path):
    """Get the position of beats and downbeats as dictionary from the text annotations

    Arguments:
        ann_path {string} -- the path of the text annotations

    Returns:
        [dict] -- a dictionary where keys are the time (string format) and the labels are either "db","b", or "bR"
    """
    ann_df = pd.read_csv(Path(ann_path),header=None, names=["time","time2","type"],sep='\t')
    out_dict = {str(a["time"]): a["type"].split(",")[0] for i,a in ann_df.iterrows()}
    return out_dict

def get_key_from_txt(ann_path):
    ann_df = pd.read_csv(Path(ann_path),header=None, names=["time","time2","type"],sep='\t')
    keys = {}
    for i, r in ann_df.iterrows():
        if len(r["type"].split(","))==3:
            number_of_sharps = int(r["type"].split(",")[2])
            key_number = key_number_from_number_of_sharps(number_of_sharps)
            keys[str(r["time"])] = [key_number, number_of_sharps]
    return keys

def midi_score_and_perf_aligned(perf_annotations_path, midi_score_annotations_path, verbose=False):
    """Check if the performance and the midi score have the same number and type of annotations

    Arguments:
        perf_annotations_path {string} -- the path of the text annotations of the performance
        midi_score_annotations_path {string} -- the path of the text annotations of the midi score

    Returns:
        boolean -- True if performance and midi score have the same annotations, false otherwise
    """
    midi_score_anns_df = pd.read_csv(Path(midi_score_annotations_path),header=None, names=["time","time2","type"],sep='\t').sort_values(by=['time'])
    perf_anns_df = pd.read_csv(Path(perf_annotations_path),header=None, names=["time","time2","type"],sep='\t').sort_values(by=['time'])
    midi_score_anns_type = [r["type"] if r["type"][-1]!= "W" else r["type"][:-1] for i, r in midi_score_anns_df.iterrows() ]
    perf_anns_type = [r["type"] if r["type"][-1]!= "W" else r["type"][:-1] for i, r in perf_anns_df.iterrows() ]
    if midi_score_anns_df.shape[0] != perf_anns_df.shape[0]:
        if verbose: print("Different length of annotations for {}: {} (ms) vs {} (perf) ".format(perf_annotations_path,len(midi_score_anns_type),len(perf_anns_type)))
        return False
    elif midi_score_anns_type == perf_anns_type: 
        return True
    else:
        if verbose:
            for ms, ms_time, perf, perf_time in zip(midi_score_anns_type,midi_score_anns_df["time"].tolist(),perf_anns_type,perf_anns_df["time"].tolist() ):
                if ms!= perf:
                    print("Different for perf {} at time {},{} : {},{}".format(perf_annotations_path,ms_time,perf_time,ms,perf))
        return False


def files_exist(row,base_path):
    fields_to_check = ['xml_score', 'midi_score','midi_performance', 'performance_annotations', 'midi_score_annotations']
    for f in fields_to_check:
        my_file = Path(base_path,row[f])
        if not my_file.is_file():
            print("File not found",my_file)


def xmlscore_parsable_music21(score_xml_path):
    """Check if we can parse the score with music21"""
    try:
        score = m21.converter.parse(score_xml_path)
    except:
        print("Problems parsing the xml score",score_xml_path )