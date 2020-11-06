import io
import os
import pathlib
import pickle


class Output(object):

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

    @staticmethod
    def save_pickle(data, path):
        """
        Save data on a file with the pickle format
        :data: data to save
        :path: path where to save the data
        """
        pathlib.Path(os.path.dirname(path)).mkdir(parents=True, exist_ok=True)
        output_stream = io.open(path, 'wb+')
        pickle.dump(data, output_stream)
        output_stream.close()


class Input(object):

    @staticmethod
    def load_pickle(path):
        input_stream = io.open(path, 'rb')
        obj_dict = pickle.load(input_stream)
        input_stream.close()
        return obj_dict