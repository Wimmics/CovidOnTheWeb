import io
import os
import pathlib


class Output(object):
    def __init__(self):
        pass

    @staticmethod
    def save_rdf(data, path):
        """
        Save data on a file with the turtle format
        :param data: data to save
        :param path: path where to save the data
        """
        pathlib.Path(os.path.dirname(path)).mkdir(parents=True, exist_ok=True)
        output_stream = io.open(path, 'bw+')
        output_stream.write(data.serialize(format='turtle'))
        output_stream.close()
