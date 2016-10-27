from .pascalvoc_util import PascalVOC

import numpy as np


pascal = PascalVOC(voc_dir='/home/lab_sd/Projects/VOCdevkit/VOC2012')


def pascal_datagen(mb_size, include_reg=True, flatten=False, separate_reg=True):
    while True:
        X, y = pascal.next_minibatch(size=mb_size)

        y_cls = y[:, :, 0]

        if separate_reg:
            y_reg = y[:, :, 1:]
        else:
            y_reg = y[:, :, :]

        y_reg = y_reg.reshape(mb_size, -1)

        if flatten:
            X = X.reshape(mb_size, -1)

        if include_reg:
            yield X, [y_cls, y_reg]
        else:
            yield X, y_cls


def pascal_datagen_singleobj(mb_size):
    while True:
        X, y = pascal.next_minibatch(size=mb_size)

        y_cls = y[:, :, 0]
        y_reg = y[:, :, 1:]

        idxes = np.argmax(y_cls, axis=1)
        y_reg = y_reg[range(mb_size), idxes]

        yield X, [y_cls, y_reg]