
import os
import sys
sys.path.append("../")
import Meta
import scipy
import scipy.io
from scipy.io import wavfile

import glob
import sphfile


# returns sent_id belongs to [ SA / SX / SI ]?
def belong_S_(sent_id):
    if sent_id <= Meta.SA_SENT_ID_RANGE[1]: return "SA"
    elif sent_id <= Meta.SX_SENT_ID_RANGE[1]: return "SX"
    else: return "SI"


# returns all [gender, sp_id] under directory (test_train + dr)
def list_dr_speakers(test_train, dr):
    all_dirs = os.listdir("{}/DR{}".format([Meta.TEST_ROOT, Meta.TRAIN_ROOT][test_train], dr))
    all_speakers = []
    for d in all_dirs:
        if d[0] == Meta.GEND[0]:
            all_speakers.append([Meta.GEND[0], d[1:]])
        elif d[0] == Meta.GEND[1]:
            all_speakers.append([Meta.GEND[1], d[1:]])

    return all_speakers


# returns all sentences spoken by a single speakers
def list_dr_speaker_sentences(test_train, dr, gender, speaker_id, S_):
    all_files = os.listdir("{}/DR{}/{}{}".format(\
        [Meta.TEST_ROOT, Meta.TRAIN_ROOT][test_train], dr, gender, speaker_id))
    sent_ids = [int(file[2:-4]) for file in all_files if (file[:2]==S_ and file[:-4])]
    return sent_ids


"""
    convert all .WAV (actually .sph files) to normal .wav files, 
    under directory (e.g. "{TEST_ROOT}/DR1/FDAC1")
"""
def convert_sph_in(directory):
    print("converting .sph to .wav under directory {}".format(directory))
    sph_files = glob.glob(directory + "*.WAV")
    for sph in sph_files:
        sphfile.SPHFile(sph).write_wav(sph.replace(".WAV", ".wav"))


# access a sentence with 2 modes
access_modes = ['wav', 'phn']
def sentence_access(test_train, dr, gender, sp_id, S_, sent_index, mode):
    prefix_name = "{}/DR{}/{}{}/{}{}".format(\
        [Meta.TEST_ROOT, Meta.TRAIN_ROOT][test_train],
        dr, gender, sp_id, S_, sent_index)
    if mode == access_modes[0]:
        x = sphfile.SPHFile(prefix_name + ".WAV").content
        return x
    elif mode == access_modes[1]:
        phones = []
        fhand = open(prefix_name + ".PHN")
        for line in fhand:
            items = line.rstrip().split()
            if len(items) == 0: break
            start, end, phone = items[0], items[1], items[2]
            phones.append([int(start), int(end), phone])
        return phones


# parse_sym
def parse_sym(sym_str):
    if sym_str in Meta.NON_PHONE: return None
    if sym_str[-1] == '1' or sym_str[-1] == '2':
        return sym_str[:-1]
    return sym_str
