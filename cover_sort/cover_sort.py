__author__ = 'anosov'

from data_processing import DataProcessing
from operator import itemgetter
import itertools
import numpy as np
from math import isnan
from fn import F, _


class CoverSort(object):
    def __init__(self, field, covers):
        self.data_processing = DataProcessing(field, covers)
        self.normalizers = list()
        self.weight = dict()

    def add_property_normalizer(self, pn, weight=1):
        self.normalizers.append(pn)
        self.weight[pn] = float(weight)

    def property_normalize(self):
        result = list()
        for pn in self.normalizers:
            item = pn(self.data_processing)
            result.append(item)
        return np.array(result, dtype=np.float32)

    def weight_normalize(self):
        weight = [self.weight[n] for n in self.normalizers]
        return np.array(weight, dtype=np.float32) / sum(weight)

    def sort(self):
        prop = self.property_normalize()
        weight = self.weight_normalize()
        norms_indexes = np.sum(prop * weight[:, None], axis=0)
        norms_raw = zip(norms_indexes, self.data_processing.covers)
        norms_without_nan = itertools.ifilterfalse(F(isnan, _[0]), norms_raw)
        norms_sorted = sorted(norms_without_nan)
        return zip(*norms_sorted)[1]