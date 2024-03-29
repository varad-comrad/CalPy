import numpy as np
from numba import jit, njit, typeof
from numba.experimental import jitclass
from typing import Self
# from imports import *
# from complex import Complex

class Array(np.ndarray):
    def __new__(cls, input_array, *, dtype=None, shape=None, order=None):
        obj = np.asarray(input_array)
        if dtype is not None:
            obj = obj.astype(dtype)
        if shape is not None:
            obj = obj.reshape(shape)
        if order is not None:
            obj = obj.copy(order=order)
        return obj.view(cls)
    
    def __call__(self, *args, **kwargs):
        values = [f(*args, **kwargs) for f in self.flat]
        return Array(values).reshape(self.shape)

    def det(self) -> float:
        return np.linalg.det(self)
    
    def find_row(self, row) -> int:
        for i, element in enumerate(self):
            if all(row[j]==element[j] for j in range(len(row))):
                return i 
        return -1

    def find_column(self, column) -> int:
        aux = self.transpose()
        return aux.find_row(column)

    def invert(self): 
        return np.linalg.inv(self)

    def to_frame(self):
        import pandas as pd
        return pd.DataFrame(data=self.array)

    def append(self,*args: tuple[list | np.ndarray], axis: str | int = 0) -> None:
        if axis == 0 or axis =='below':
            final = self.__below_append(*args)
        elif axis == 1 or axis =='right':
            final = self.__right_append(*args)
        else:
            raise ValueError
        return final

    def __below_append(self,*args: tuple[list | np.ndarray]):
        for element in args:
            if not isinstance(element, list | np.ndarray):
                raise TypeError(f"Invalid type: {type(element)}")
            elif len(element) != len(self[0]):
                raise TypeError()
        original_size = len(self)
        final_size = len(self) + len(args)
        self.resize((final_size,len(self[0])))
        for i, element in enumerate(args):
            self[original_size+i] = np.array(element)

    def __right_append(self,*args: tuple[list | np.ndarray]):
        aux = self.transpose().copy()
        aux.append(*args)
        self = aux.transpose()


    def solve(self, b):
        return np.linalg.solve(self, b)


if __name__ == '__main__':
    pass