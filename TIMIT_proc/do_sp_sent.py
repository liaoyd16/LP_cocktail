# 2. table: {speaker} x S_, sentence id
# dumped to "tablejsons/"
# structure: speaker_id x edge, edge x sent_id

import sys
sys.path.append("../")
import Meta
import utils.sentence_access as access
import os
import json
import config

# table structure: dict[sp_id] -> array(|sentences|)

def add(table, sp_id, sent_ids):
    table[sp_id] = sent_ids


def do_sp_sent():
    print("do speaker_sentence table")
    speaker_info = json.load(open(os.path.join(Meta.PROJ_ROOT, "TIMIT_proc/docjsons/speaker_info.json")))
    
    table = dict()
    for speaker_id in speaker_info: # (speaker_id, gender, test_train, dr)
        info = speaker_info[speaker_id]
        gender = info[0]
        test_train = info[1]
        dr = info[2]
        sent_ids = access.list_dr_speaker_sentences(\
                        test_train, dr, gender, speaker_id, config.S_)
        add(table, speaker_id, sent_ids)

    json.dump(table, open(os.path.join(Meta.PROJ_ROOT, "TIMIT_proc/tablejsons/sp_sent_table.json"), "w"))


if __name__ == '__main__':
    do_sp_sent()