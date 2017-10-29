import os
from os.path import *
import json


class Configs(object):
    def __init__(self, json_fname=None):
        """
        Constructor - takes options
        :param json_fname:{str} path to json file containing path definitions
        """
        self.NSIS_EXE_PATH = ''
        self.CMAKE_PATH = ''
        self.CMAKE_GENERATOR_NAME = ''
        self.WIN_INSTALLER_CREATOR = ''
        self.PYQT_VERSION = ''
        self.WIN_DEPENDENCIES_ROOT = ''
        self.PYTHON_DIR = ''
        self.PYTHON_EXECUTABLE = ''
        self.PYTHON_INCLUDE_DIR = ''
        self.PYTHON_LIBRARY = ''
        self.VTK_DIR = ''
        self.OPENCL_LIBRARIES = ''

        if json_fname:
            self.load_configs(json_fname=json_fname)

    def load_configs(self, json_fname):
        """
        initializes config paths based on json file
        :param json_fname: {str}  path to json file containing path definitions
        :return: None
        """
        attr_dict = {key: value for key, value in self.__dict__.items() if
                     not key.startswith("__") and isinstance(value, str)}

        with open(json_fname) as data_file:
            jn = json.load(data_file)

        for key, value in attr_dict.items():

            print 'key, value=', (key, value)
            try:
                json_value = jn[key]
            except KeyError:
                print ('Could not find "{}" in {}'.format(key, json_fname))

            try:
                attr = getattr(self, key)
                setattr(self, key, json_value)
            except AttributeError:
                print('Could not find attribute "{}" in {} - defined in file {}'.format(key, self.__class__.__name__,
                                                                                        __file__))
        print


if __name__ == '__main__':
    conf = Configs()
    conf.load_configs(json_fname=join(dirname(__file__), 'config_64bit.json'))
