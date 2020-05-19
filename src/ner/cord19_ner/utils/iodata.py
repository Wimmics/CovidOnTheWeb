import io
import os
import json
import csv
import pathlib


class Input(object):
    def __init__(self):
        pass

    @staticmethod
    def load_csv(path):
        """
        Load data contained in a csv file
        :param path: data path
        :return obj: data contained in a DictReader
        """
        input_stream = io.open(path, 'r')
        obj = csv.DictReader(input_stream)
        return obj


class Output(object):
    def __init__(self):
        pass

    @staticmethod
    def save_json(data, path):
        """
        Save data on a file with the json format
        :param data: data to save
        :param path: path where to save the data
        """
        pathlib.Path(os.path.dirname(path)).mkdir(parents=True, exist_ok=True)
        output_stream = io.open(path, 'w+')
        json.dump(data, output_stream, ensure_ascii=False, indent=4)
        output_stream.close()

