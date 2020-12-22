# 6. (phoneme, gender) x (phoneme, gender) |=> (distort, mute)

import os
import sys
sys.path.append("../model")
sys.path.append("../utils")

import Meta
import model.do_model
import sentence_access as access
import metrics

import json
import numpy as np
import itertools


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

    # src: 2, tgt: 1
    for phone_1, phone_2 in itertools.product(phones_info, phones_info):
        sym_1 = phone_1[1]
        sym_2 = phone_2[1]
        for igen1, igen2 in itertools.product(range(2), range(2)):
            pairs = phone_gender_pair[sym_1][sym_2][igen1][igen2]
            for isent in range(len(pairs)):
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
                    sent1_info['sp_id'], S_1, sent1_id, mode='wav')
                sent_src = access.sentence_access(\
                    sent2_info['test_train'], sent2_info['dr'], sent2_info['gender'], \
                    sent2_info['sp_id'], S_2, sent2_id, mode='wav')

                """ do hierarchical conversion here: """
                x_convert = model.model(sent_tgt, sent_src, 512)
                distort = metrics.distortion(x_convert, sent_tgt, sent_src)
                mute = metrics.mute(x_convert, sent_src)

                add(table, phone_1, phone_2, igen1, igen2, [x_convert, distort, mute])

    json.dump(table, open(os.path.join(Meta.PROJ_ROOT, "TIMIT_proc/resultjsons/results.json"), "w"))


if __name__ == '__main__':
    do_phone_gender_vals()
