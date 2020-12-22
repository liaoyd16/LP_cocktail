# 3. table: phoneme x sentence id |=> duration_bound
# dumped to "tablejsons/"

import os
import sys
sys.path.append("../")
import Meta
import utils.sentence_access as access
import json
import config

# table structure: dict[sent_id] -> dict[phone] -> array(2)

def add(table, sym, sent_id, dur):
    if sent_id not in table:
        table[sent_id] = dict()
    if sym not in table[sent_id]:
        table[sent_id][sym] = dur   # note first appearance

def do_phone_sentdur():
    print("do phone_sent_dur table")
    speaker_info = json.load(open(os.path.join(Meta.PROJ_ROOT, "TIMIT_proc/docjsons/speaker_info.json")))

    table = dict()
    for speaker_id in speaker_info: # (speaker_id => gender, test_train, dr)
        info = speaker_info[speaker_id]
        gender = info[0]
        test_train = info[1]
        dr = info[2]
        sent_ids = access.list_dr_speaker_sentences(\
                        test_train, dr, gender, speaker_id, S_=config.S_)
        for sent_id in sent_ids:
            phn = access.sentence_access(test_train, dr, gender, speaker_id, "SI", sent_id, mode="phn")
            for dur_sym in phn:
                # !: filter out 'others' symbols & stress markers
                sym = access.parse_sym(dur_sym[2])
                if not sym == None:
                    dur = [dur_sym[0], dur_sym[1]]
                    add(table, sym, sent_id, dur)

    json.dump(table, open(os.path.join(Meta.PROJ_ROOT, "TIMIT_proc/tablejsons/phone_sentdur.json"), "w"))
    

if __name__ == '__main__':
    do_phone_sentdur()