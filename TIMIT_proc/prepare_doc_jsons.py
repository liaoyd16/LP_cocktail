
# prepare jsons that store doc info
# 1. [(speaker_id, gender, dr, test_train)]
# 2. all phones
# dumped to "docjsons/"

import __init__
from __init__ import *
import json
import utils
import utils.sentence_access as access
import itertools


def do_speaker_info():
    print("collecting speaker info")
    speaker_info_dict = dict()
    all_DR = range(1, Meta.NUM_DR+1)
    for test_train, dr in itertools.product([0,1], all_DR):
        print("\tscanning {}, dr={}".format(["TEST", "TRAIN"][test_train], dr))
        all_sp_info = access.list_dr_speakers(test_train, dr)
        for sp_info in all_sp_info:
            speaker_info_dict[sp_info[1]] = [sp_info[0], test_train, dr]

    # (speaker_id: gender, test_train, dr)
    if Meta_config.WIN:
        json.dump(speaker_info_dict, open(os.path.join(Meta.PROJ_ROOT, "TIMIT_proc\\docjsons\\speaker_info.json"), "w"))
    else:
        json.dump(speaker_info_dict, open(os.path.join(Meta.PROJ_ROOT, "TIMIT_proc/docjsons/speaker_info.json"), "w"))


def input_phones():
    # input "{} {}".format(type, symbol)
    # ends with empty line
    print("collecting all (meaningful) phones")
    phones = []
    if Meta_config.WIN:
        filename = os.path.join(Meta.PROJ_ROOT, "TIMIT_proc\\docjsons\\phonecode.txt")
    else:
        filename = os.path.join(Meta.PROJ_ROOT, "TIMIT_proc/docjsons/phonecode.txt")
    for s in open(filename):
        items = s.rstrip().split()
        assert(len(items) == 2)
        phones.append([items[0], items[1]])

    if Meta_config.WIN:
        json.dump(phones, open(os.path.join(Meta.PROJ_ROOT, "TIMIT_proc\\docjsons\\phones.json"), "w"))
    else:
        json.dump(phones, open(os.path.join(Meta.PROJ_ROOT, "TIMIT_proc/docjsons/phones.json"), "w"))


if __name__ == '__main__':
    input_phones()
    # do_speaker_info()
