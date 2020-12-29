
import __init__
from __init__ import *
import ArrayTree
import components
from components import do_levdur, do_decomp_tree, do_comb_tree
import datetime

def do_model(eng, x_tgt, x_src, nfft):
    """
        eng argument:
        - initialized & passed from do_phone_gender_val.py::do_phone_gender_val(...)
        - passed into components.do_*(..., eng=eng) as last argument
        - in module components.py: eng used as first argument in _do_*(eng, ...)
    """
    l_sum = len(x_tgt)+len(x_src)
    print("\t\t\ttask load: {}, {}ms".format(l_sum, l_sum/Meta.Fs*1000))
    print("\t\t\t decomp src: {}".format( str(datetime.datetime.now()) ))
    xtree_src = do_decomp_tree(x_src, 2, 2, 512, eng=eng)
    print("\t\t\t decomp tgt: {}".format( str(datetime.datetime.now()) ))
    xtree_tgt = do_decomp_tree(x_tgt, 2, 2, 512, eng=eng)

    print("\t\t\t lev-dur: {}".format( str(datetime.datetime.now()) ))
    atree_tgt = do_levdur(xtree_tgt, 512, eng=eng)
    # atree_src = do_levdur(xtree_src, 512, eng=eng)

    print("\t\t\t comb: {}".format( str(datetime.datetime.now()) ))
    new_xtree = do_comb_tree(xtree_src, nfft, atree_tgt=atree_tgt, atree_src=None, eng=eng) # try: atree_src = None
    x_ans = new_xtree.get(0, 0)

    return x_ans