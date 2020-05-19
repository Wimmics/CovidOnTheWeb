class Converter(object):

    def __init__(self, params):
        pass

    @staticmethod
    def string2number(value):
        """
        Convert a string to a number
        :param value: string to convert
        :return: integer, float or string
        """
        try:
            return int(value)
        except ValueError:
            try:
                return float(value)
            except ValueError:
                if isinstance(value, list):
                    value = str(value)
                return value

