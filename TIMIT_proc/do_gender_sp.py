# 1. table: {speaker} <= gender
# dumped to "tablejsons/"

import os
import sys
sys.path.append("../")
import Meta
from Meta import GEND
import json

# table structure: dict(gender) -> array(n_speakers)

def do_gender_sp():
    table = {GEND[0]:set(), GEND[1]:set()}
    print("do {speaker} <= gender table")
    speaker_info = json.load(open(os.path.join(Meta.PROJ_ROOT, "TIMIT_proc/docjsons/speaker_info.json")))

    for sp_id in speaker_info: # (speaker_id: gender, test_train, dr)
        gender = speaker_info[sp_id][0]
        if gender == GEND[0]: table[GEND[0]].add(sp_id)
        else:                 table[GEND[1]].add(sp_id)

    table[GEND[0]] = list(table[GEND[0]])
    table[GEND[1]] = list(table[GEND[1]])
    json.dump(table, 
        open(os.path.join(Meta.PROJ_ROOT, "TIMIT_proc/tablejsons/gender_sp_table.json"), "w")
    )

if __name__ == '__main__':
    do_gender_sp()