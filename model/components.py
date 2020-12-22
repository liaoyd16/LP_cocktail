
import numpy as np
import statsmodels
from statsmodels.tsa.stattools import levinson_durbin
import copy

import matlab
import matlab.engine


global eng

def start_matlab():
    global eng
    eng = matlab.engine.start_matlab()

def quit_matlab():
    global eng
    eng.quit()

def _do_combine2(xs, nfft):
    if len(xs) != 2: raise NotImplementedError()
    xlow = xs[0]
    xhigh = xs[1]
    x_rec = eng.compose2(xlow, xhigh, nfft, nargout=1)
    return x_rec


def _do_decomp2(x, nfft):
    xs = eng.decompose2(x, nfft, nargout=2)
    return xs


err_list = []

def _do_levdur_array(x):
    err, arcoeff, _, _, _ = levinson_durbin(x)
    err_list.append(err)
    return arcoeff

def _convert(x, a_tgt, a_src=None):
    """
        given x and a_tgt, a_src, try:
        i) whiten x with a_src
           if a_src==None: skip i)
        ii) color x with a_tgt
    """
    global eng
    if not a_src == None:
        x = np.convolve(x, np.concatenate([[1], -a_src])) # do whitening: a_src
    k = eng.tf2latc(1, matlab.double(a_tgt))              # do IIR: a_tgt
    f, _ = eng.latcfilt(k, x, nargout=2)
    return np.array(f)

def _do_filter_at(l, k, xtree, atree_tgt, atree_src):
    """
        given xtree and atree_tgt, atree_src, 
        call `_convert` for tree position (l,k)
        `_convert` tries to:
        i) whiten xtree::node with corresponding
           atree_src::nodes
           if atree_src==None: skip i)
        ii) color xtree::node with 
           atree_tgt::node
    """
    x = xtree.get(l, k)
    a_tgt = atree_tgt.get(l, k)
    if atree_src == None: filtered = _convert( x, a_tgt )
    else:
        a_src = atree_src.get(l, k)
        filtered = _convert( x, a_tgt, a_src )
    return filtered


def do_decomp_tree(x, L, base, nfft):
    """
        decompose original array -> create a tree
        traverse from root (0,0), in BFS fashion
        when inner nodes are traversed, `base` 
        children are created; leafs are not traversed
    """
    xtree = ArrayTree(base)
    xtree.add_root(x)
    for l in range(L-1):
        for k in range(base**l):
            x_parent = xtree.get(l, k)
            x_children = _do_decomp2(x_parent, nfft)
            for ix in range(len(x_children)):
                xtree.add_child((l,k), ix, x_children[ix])

    return xtree


def do_levdur(xtree, nfft):
    """
        do levinson_durbin algorithm at every node
        in xtree, using _do_levdur_array for each
        node
    """
    L = xtree.num_layers
    base = xtree.get_base
    atree = ArrayTree(base)
    for l in range(L):
        for k in range(base**l):
            x = xtree.get(l, k)
            a = _do_levdur_array(x)
            atree.add_child( atree.get_parent_pos(l, k), k % base, a )

    return atree


def do_comb_tree(xtree, nfft, atree_tgt, atree_src=None):
    """
        filter xtree with i) atree_tgt, ii) atree_src
        from bottom (leaves) to top (root)
        ---
        atree_src: optional, not None if whitening is
                   applied
    """
    Lx = xtree.num_layers
    La_t = atree_tgt.num_layers
    assert(Lx==La_t)
    if not atree_src == None:
        La_s = atree_src.num_layers
        assert(Lx==La_s)
    L = Lx

    base_x = xtree.get_base
    base_a_t = atree_tgt.get_base
    assert(base_a_t == base_x)
    if not atree_src == None:
        base_a_s = atree_src.get_base
        assert(base_a_s == base_x)
    base = base_x

    new_xtree = ArrayTree(base, init_layers=L)

    for k in range(2**(L-1)):
        new_xtree.get_write(L-1, k, xtree.get(L-1, k))

    for l in np.arange(L, 1, -1) - 1: # layers: L-1, ..., 1
        for k in range(2**l):
            filtered = _do_filter_at(l, k, xtree, atree_tgt, atree_src)
            new_xtree.get_write(l, k, filtered)
        for k in range(2**(l-1)):
            comb = _do_combine2(\
                [new_xtree.get(new_xtree.get_child_pos((l-1,k),nth)) for nth in range(base)], \
                nfft)
            new_xtree.get_write(l-1, k, comb)

    # filtering at original scale
    filtered = _do_filter_at(0, 0, xtree, atree_tgt, atree_src)
    new_xtree.get_write(0, 0, filtered)

    return new_xtree

