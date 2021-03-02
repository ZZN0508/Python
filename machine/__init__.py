# -*- coding: utf-8 -*-
from CurveFitting import cureFitting,image_rendering;
import itertools;
if __name__ == '__main__':
    #list_random=list(itertools.product(range(-10, 10),range(-10, 10)));
    list_random=[[-3, 9], [-3, 9], [3, 9], [-1, 1]]
    list_value=cureFitting(4, list_random);
    print(list_value);
    # image_rendering(list_random,list_value);