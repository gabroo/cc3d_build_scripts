import os
from os.path import *
import json


class ConfigsBase(object):
    def __init__(self, json_fname=None):

        """
        Constructor - takes config json file and initializes paths
        :param json_fname:{str} path to json file containing path definitions
        """
        self.json_fname = json_fname

    def load_configs(self, json_fname):
        """
        initializes config paths based on json file
        :param json_fname: {str}  path to json file containing path definitions
        :return: None
        """
        attr_dict = {key: value for key, value in self.__dict__.items() if
                     not key.startswith("__") and isinstance(value, str) and key != 'json_fname'}

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

    def initialize(self):
        if self.json_fname:
            self.load_configs(json_fname=self.json_fname)


# class ConfigsWindows(object):
#     def __init__(self, json_fname=None):
#         """
#         Constructor - takes options
#         :param json_fname:{str} path to json file containing path definitions
#         """

class ConfigsWindows(ConfigsBase):
    def __init__(self, json_fname=None):
        """
        Constructor - takes config json file and initializes paths
        :param json_fname:{str} path to json file containing path definitions
        """
        ConfigsBase.__init__(self, json_fname)

        self.NSIS_EXE_PATH = ''
        self.CMAKE_PATH = ''
        self.CMAKE_GENERATOR_NAME = ''
        self.WIN_INSTALLER_CREATOR = ''
        self.WIN_INSTALLER_TEMPLATE = ''
        self.BUILD_ARCH_TAG = ''
        self.PYQT_VERSION = ''
        self.WIN_DEPENDENCIES_ROOT = ''
        self.PYTHON_DIR = ''
        self.PYTHON_EXECUTABLE = ''
        self.PYTHON_INCLUDE_DIR = ''
        self.PYTHON_LIBRARY = ''
        self.VTK_DIR = ''
        self.OPENCL_LIBRARIES = ''

        self.initialize()


class ConfigsOSX(ConfigsBase):
    def __init__(self, json_fname=None):
        """
        Constructor - takes config json file and initializes paths
        :param json_fname:{str} path to json file containing path definitions
        """
        ConfigsBase.__init__(self, json_fname)

        self.PYTHON_MINOR_VERSION = ''
        self.CMAKE_PATH = ''
        self.CMAKE_GENERATOR_NAME = ''
        self.CMAKE_OSX_DEPLOYMENT_TARGET = ''
        self.PYQT_VERSION = ''
        self.PREREQUISITES_DIR = ''
        self.PYTHON_EXECUTABLE = ''
        self.PYTHON_INCLUDE_DIR = ''
        self.PYTHON_LIBRARY = ''
        self.VTK_DIR = ''
        self.CMAKE_C_COMPILER = ''
        self.CMAKE_C_FLAGS = ''
        self.CMAKE_CXX_COMPILER = ''
        self.CMAKE_CXX_FLAGS = ''
        self.RR_INSTALL_PATH = ''


        self.initialize()


if __name__ == '__main__':
    conf = ConfigsWindows()
    conf.load_configs(json_fname=join(dirname(dirname((__file__))), 'windows', 'build_scripts', 'config_64bit.json'))
