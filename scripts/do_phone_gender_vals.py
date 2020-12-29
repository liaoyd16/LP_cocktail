# 6. (phoneme, gender) x (phoneme, gender) |=> (distort, mute)

import __init__
from __init__ import *
from model.model import do_model
import model.components
import utils.sentence_access as access
import metrics
import json
import numpy as np
import itertools

import matlab
import matlab.engine

""" matlab api """
def start_matlab():
    eng = matlab.engine.start_matlab()
    eng.cd(os.path.join(Meta.PROJ_ROOT, "model/"), nargout=0)
    return eng

def quit_matlab(eng):
    eng.quit()


def add(table, phone_1, phone_2, igen1, igen2, x_distort_mute):
    if phone_1 not in table:
        table[phone_1] = dict()
    if phone_2 not in table[phone_1]:
        table[phone_1][phone_2] = [[[],[]],[[],[]]]
    table[phone_1][phone_2][igen1][igen2].append(x_distort_mute)

def do_phone_gender_vals():
    phones_info = json.load(open(os.path.join(Meta.PROJ_ROOT, "TIMIT_proc/docjsons/phones.json")))
    phone_gender_pair = json.load(open(os.path.join(Meta.PROJ_ROOT, "TIMIT_proc/tablejsons/phone_gender_pair.json")))

    table = dict()

    print("scanning all sym-gender pairs")
    # src: 2, tgt: 1
    eng = start_matlab()
    for phone_1, phone_2 in itertools.product(phones_info[32:34], phones_info[32:34]):
        print("\tphone1 = {}, phone2 = {}".format(phone_1, phone_2))
        sym_1 = phone_1[1]
        sym_2 = phone_2[1]
        for igen1, igen2 in itertools.product(range(2), range(2)):
            print("\t\tgen1 = {}, gen2 = {}".format(Meta.GEND[igen1], Meta.GEND[igen2]))
            pairs = phone_gender_pair[sym_1][sym_2][igen1][igen2]
            for isent in range(len(pairs)):
                print("\t\t\tsent pair = #{}".format(isent))
                pair = pairs[isent]
                sent1_info, sent2_info = pair[0], pair[3]

                sent1_id = sent1_info['sent_id']
                sent2_id = sent2_info['sent_id']
                S_1 = access.belong_S_(sent1_id)
                S_2 = access.belong_S_(sent2_id)
                dur1 = (pair[1], pair[2])
                dur2 = (pair[4], pair[5])

                sent_tgt = access.sentence_access(\
                    sent1_info['test_train'], sent1_info['dr'], sent1_info['gender'], \
                    sent1_info['sp_id'], S_1, sent1_id, mode='wav')[dur1[0]: dur1[1]]
                sent_src = access.sentence_access(\
                    sent2_info['test_train'], sent2_info['dr'], sent2_info['gender'], \
                    sent2_info['sp_id'], S_2, sent2_id, mode='wav')[dur2[0]: dur2[1]]

                """ do hierarchical conversion here: """
                x_convert = do_model(eng, sent_tgt, sent_src, 512)
                # print(len(x_convert), len(sent_tgt), len(sent_src))
                distort = -1# metrics.distortion(x_convert, sent_tgt, sent_src)
                mute = metrics.mute(x_convert, sent_src)

                add(table, sym_1, sym_2, igen1, igen2, [sent_tgt.tolist(), x_convert.tolist(), sent_src.tolist(), distort, mute])

    quit_matlab(eng)
    if Meta_config.WIN:
        json.dump(table, open(os.path.join(Meta.PROJ_ROOT, "TIMIT_proc\\resultjsons\\results.json"), "w"))
    else:
        json.dump(table, open(os.path.join(Meta.PROJ_ROOT, "TIMIT_proc/resultjsons/results.json"), "w"))


if __name__ == '__main__':
    do_phone_gender_vals()