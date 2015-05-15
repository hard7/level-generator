__author__ = 'anosov'
from data_processing import DataProcessing

def norm_len_path():
    def wrapper(data):
        assert isinstance(data, DataProcessing)
        lp = data.len_path