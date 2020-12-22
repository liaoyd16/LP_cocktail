
import ArrayTree
import components
from components import do_levdur, do_decomp_tree, do_comb_tree

def do_model(x_tgt, x_src, nfft):
    xtree_src = do_decomp_tree(x_src)
    xtree_tgt = do_decomp_tree(x_tgt)
    
    atree_tgt = do_levdur(xtree_tgt)
    # atree_src = do_levdur(xtree_src)

    new_xtree = do_comb_tree(xtree_src, nfft, atree_tgt) # try: atree_src = None
    x_ans = new_xtree.get(0, 0)

    return x_ans