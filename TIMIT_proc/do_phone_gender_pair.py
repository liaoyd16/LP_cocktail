# 5. table: (phoneme, gender) x (phoneme, gender) |=> (s1,d1,s2,d2)
# dumped to "tablejsons/"

import __init__
from __init__ import *
import utils.sentence_access as access
import json
import itertools

import do_phone_gender_sentdur


# table structure: dict[phone_1] -> dict[phone_2] -> array[2,2]

def add(table, phone_1, phone_2, igen1, igen2, sd1_sd2_list):
    if phone_1 not in table:
        table[phone_1] = dict()
    if phone_2 not in table[phone_1]:
        table[phone_1][phone_2] = [[None,None],[None,None]]
    table[phone_1][phone_2][igen1][igen2] = sd1_sd2_list


def do_phone_gender_pair():
    if Meta_config.WIN:
        phones_info = json.load(open(os.path.join(Meta.PROJ_ROOT, "TIMIT_proc\\docjsons\\phones.json")))
        phone_gender_sentdur = json.load(open(os.path.join(Meta.PROJ_ROOT, "TIMIT_proc\\tablejsons\\phone_gender_sentdur.json")))
    else:
        phones_info = json.load(open(os.path.join(Meta.PROJ_ROOT, "TIMIT_proc/docjsons/phones.json")))
        phone_gender_sentdur = json.load(open(os.path.join(Meta.PROJ_ROOT, "TIMIT_proc/tablejsons/phone_gender_sentdur.json")))

    table = dict()

    for phone_1, phone_2 in itertools.product(phones_info,phones_info):
        sym1 = phone_1[1]
        sym2 = phone_2[1]
        for igen1, igen2 in itertools.product(range(2), range(2)):
            gen1_sent_dur_n = phone_gender_sentdur[sym1][igen1]
            gen2_sent_dur_n = phone_gender_sentdur[sym2][igen2]
            sd1_sd2_list = []
            for i in range(len(gen1_sent_dur_n)):
                sd1_sd2_list.append([*gen1_sent_dur_n[i], *gen2_sent_dur_n[::-1][i]]) # reverse order for list #2
            add(table, sym1, sym2, igen1, igen2, sd1_sd2_list)

    if Meta_config.WIN:
        json.dump(table, open(os.path.join(Meta.PROJ_ROOT, "TIMIT_proc\\tablejsons\\phone_gender_pair.json"), "w"))
    else:
        json.dump(table, open(os.path.join(Meta.PROJ_ROOT, "TIMIT_proc/tablejsons/phone_gender_pair.json"), "w"))


if __name__ == '__main__':
    do_phone_gender_pair()