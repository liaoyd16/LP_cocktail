
import numpy as np

class ArrayTree:
    """docstring for ArrayTree"""
    def __init__(self, base, init_layers=0):
        
        self.base = base
        if init_layers == 0:
            self.layers = []
        else:
            self.layers = [[None for _ in range(base**l)] for l in range(init_layers)]
    
    @property
    def num_layers(self):
        return len(self.layers)

    @property
    def get_base(self):
        return self.base


    def _check_legal(self, l, k):
        assert(l < len(self.layers) and 0 <= k and k < self.base**l)


    def get(self, l, k):
        self._check_legal(l, k)
        return self.layers[l][k]

    def get_write(self, l, k, x):
        self._check_legal(l, k)
        self.layers[l][k] = x

    def get_parent_pos(self, l, k):
        return (l-1, int(k//self.base))

    def get_child_pos(self, lk, nth): # l starts from 0, k starts from 0
        l, k = lk
        return (l+1, self.base*k+nth)


    def add_child(self, lk, nth, x): # (l,k) is the parent, l starts from 0, k starts from 0
        l, k = lk
        assert(l < len(self.layers))
        if len(self.layers) == l+1:
            self.layers.append([None for _ in range(self.base**(l+1))])
        l_child, k_child = self.get_child_pos( (l,k), nth )
        self.layers[l_child][k_child] = x

    def add_root(self, x):
        self.layers = [[x]]

