# 4. table: phoneme x gender |=> (sentence, duration_bound)
# dumped to "tablejsons/"

import __init__
from __init__ import *
import json
import random


# table structure: dict[sym] -> array[2] -> list(n)

def add(table, sym, igender, sent_durs):
    # add a complete line
    if sym not in table:
        table[sym] = [None, None]
    table[sym][igender] = sent_durs


# table1: gender_sp / table3: phone_sentdur / table2: sp_sent
def lookup(speaker_info, gender_sp, phone_sentdur, sp_sent, gender, sym, num):
    sp_candids = gender_sp[gender]

    picked_sentdur = []
    cnt = 0
    for candid in sp_candids:           # traverse speakers of this gender
        sent_id_candids = []
        for sent_id in sp_sent[candid]: # filter sentences by this speaker, that contains `sym`
            if sym in phone_sentdur[str(sent_id)]:
                sent_id_candids.append(sent_id)

        if len(sent_id_candids) > 0:    # randomly choose a sentence among `sent_id_candids`
            pick_sent_id = random.choice(sent_id_candids)
            info = speaker_info[candid]
            test_train, dr = info[1], info[2] # <- candid
            pick_sent_info = {'test_train': test_train, 'dr': dr, 'gender': gender, 'sp_id': candid, 'sent_id': pick_sent_id}
            picked_sentdur.append([pick_sent_info, *phone_sentdur[str(pick_sent_id)][sym]]) # add sentence-duration
            cnt += 1
            if cnt == num: break

    try:
        assert(len(picked_sentdur) == num)
    except:
        print(sym, gender, len(picked_sentdur))

    return picked_sentdur


def do_phone_gender_sentdur():
    print("do phone_gender_sent_dur table")

    if Meta_config.WIN:
        speaker_info = json.load(open(os.path.join(Meta.PROJ_ROOT, "TIMIT_proc\\docjsons\\speaker_info.json")))
        phones_info = json.load(open(os.path.join(Meta.PROJ_ROOT, "TIMIT_proc\\docjsons\\phones.json")))
        gender_sp = json.load(open(os.path.join(Meta.PROJ_ROOT, "TIMIT_proc\\tablejsons\\gender_sp_table.json")))
        phone_sentdur = json.load(open(os.path.join(Meta.PROJ_ROOT, "TIMIT_proc\\tablejsons\\phone_sentdur.json")))
        sp_sent = json.load(open(os.path.join(Meta.PROJ_ROOT, "TIMIT_proc\\tablejsons\\sp_sent_table.json")))
    else:
        speaker_info = json.load(open(os.path.join(Meta.PROJ_ROOT, "TIMIT_proc/docjsons/speaker_info.json")))
        phones_info = json.load(open(os.path.join(Meta.PROJ_ROOT, "TIMIT_proc/docjsons/phones.json")))
        gender_sp = json.load(open(os.path.join(Meta.PROJ_ROOT, "TIMIT_proc/tablejsons/gender_sp_table.json")))
        phone_sentdur = json.load(open(os.path.join(Meta.PROJ_ROOT, "TIMIT_proc/tablejsons/phone_sentdur.json")))
        sp_sent = json.load(open(os.path.join(Meta.PROJ_ROOT, "TIMIT_proc/tablejsons/sp_sent_table.json")))

    table = dict()
    for type_sym in phones_info:
        sym = type_sym[1]
        for igender in range(2):
            sent_durs = lookup(speaker_info, gender_sp, phone_sentdur, sp_sent, gender=Meta.GEND[igender], sym=sym, num=5)
            add(table, sym, igender, sent_durs)

    if Meta_config.WIN:
        json.dump(table, open(os.path.join(Meta.PROJ_ROOT, "TIMIT_proc\\tablejsons\\phone_gender_sentdur.json"), "w"))
    else:
        json.dump(table, open(os.path.join(Meta.PROJ_ROOT, "TIMIT_proc/tablejsons/phone_gender_sentdur.json"), "w"))


if __name__ == '__main__':
    do_phone_gender_sentdur()
